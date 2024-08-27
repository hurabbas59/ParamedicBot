import os
from src.utils.qdrant_utils import QdrantUtils
from src.utils.pdf_parsers import PdfParser
from src.utils.prompts import query_prompt_template
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


qdrant_client = QdrantUtils()

def get_responder_type(res_file_path):
    responsders_type = ["EMT-Basic","AEMT","First Responder","Paramedic"]
    responders = res_file_path.split("/")
    for res_type in responsders_type:
        if res_type in responders:
            return res_type

    return None

def get_state(state_path):
    states = state_path.split("/")

    for state in states:

        if len(state)==2:
            return state

    return None

async def upsert_vectors_to_qdrant():

    root_dir = "KB"
    # folders = ["General Information","Specific Files","Combo Files/Local Combo","Combo Files/National Combo","Combo Files/State Combo","Specialty"]
    folders = ['Combo Files/Local Combo']

    try:
        for fold in folders:

            for root, dirs, files in os.walk(os.path.join(root_dir,fold)):
                for file in files:
                    local_file_path = os.path.join(root,file)

                    if local_file_path.endswith('.pdf'):
                        parser = PdfParser(local_file_path)
                        paragraphs = parser.parse()

                        metadata = [{"type":get_responder_type(local_file_path),
                                    "state":get_state(local_file_path)
                                    } for _ in range(len(paragraphs))]
                        
                        qdrant_client.upsert_vectors(collection_name='-'.join(fold.split("/")),
                                                    documents=paragraphs,
                                                    metadata=metadata
                                                    )

                        del paragraphs
                        del metadata

    except Exception as e:
        print(f"Exception occured {e}")
        return {
            "status":"500",
            "message":f"Excpetion {e}"
        }
    
    return {
        "status":"200",
        "message":"Success"

    }
    
async def ask_query(query: str, license_level: str, state: str):
    llm = ChatOpenAI(api_key="")
    prompt_template = PromptTemplate(template=query_prompt_template,input_variables=["context","query"])
    chain = LLMChain(llm=llm,prompt=prompt_template)

    # retreive context
    context = qdrant_client.search_docs(query=query,state=state,license_level=license_level)

    response = chain.invoke({"context":context,"query":query})
    return response['text']
