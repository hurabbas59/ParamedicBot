from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.services import upsert_vectors_to_qdrant, ask_query
from src.schema.pydantic_models import UploadResponse, QueryRequest, QueryResponse

app = FastAPI()




@app.get("/upload_vectors")
async def upload_vectors():
    response = await upsert_vectors_to_qdrant()
    print(response)
    return {"status":200}

@app.post("/query",response_model=QueryResponse)
async def query(input: QueryRequest):

    response = await ask_query(query=input.query,
                               license_level=input.license_level,
                               state=input.state)
    
    return QueryResponse(response=response)
    

# Allow requests from localhost during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)