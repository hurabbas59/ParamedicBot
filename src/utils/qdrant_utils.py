from qdrant_client import QdrantClient
from typing import List
import uuid
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from langchain_openai import OpenAIEmbeddings

class QdrantUtils:

    def __init__(self,path: str = "./KB-Vector-Store/"):
        self.client = QdrantClient(path=path)  # Persists changes to disk
        self.vector_size = 1536
        self.emb_model = OpenAIEmbeddings(api_key="")


    def is_collection_exits(self,collection_name: str):
        collections = [collection.name for collection in self.client.get_collections().collections]

        if collection_name in collections:
            return True
        
        return False

    def upsert_vectors(self,collection_name: str, documents: List[str], metadata: List[dict]):
       
       if documents:

            try:

                if self.is_collection_exits(collection_name):
                    print("Upserting in existing")
                    points = []
                    for doc, meta in zip(documents,metadata):
                        vector = self.emb_model.embed_query(doc)
                        meta['text'] = doc
                        points.append(PointStruct(id=str(uuid.uuid4()),payload=meta,vector=vector))

                    self.client.upsert(collection_name=collection_name,points=points)

                else:
                    # Create New Collection
                    print("creating a collection")
                    self.client.create_collection(collection_name=collection_name,
                            vectors_config=VectorParams(size=self.vector_size,distance=Distance.COSINE))
                    
                    points = []
                    for doc, meta in zip(documents,metadata):
                        vector = self.emb_model.embed_query(doc)
                        meta['text'] = doc
                        points.append(PointStruct(id=str(uuid.uuid4()),payload=meta,vector=vector))

                    self.client.upsert(collection_name=collection_name,points=points)

            except Exception as e:
                print(f"Exception Occured {e}")
            

    def search_docs(self,query: str, license_level: str, state: str,limit: int =10):

        vector = self.emb_model.embed_query(query)
        # Search for every collection with filter of State and License when Specific Files

        collections = [
            {"file":"Combo Files-Local Combo","must_state":True,"license_level": False},
            {"file":"Combo Files-State Combo","must_state":True,"license_level": False},
            {"file":"Specific Files","must_state":True,"license_level": True},
            {"file":"Combo Files-National Combo","must_state":False,"license_level": False},
            {"file":"General Information","must_state":False, "license_level": False},
            {"file":"Specialty","must_state":False,"license_level": False},
            


        ]

        documents = []
        for collection in collections:
            if collection['file'] in ["Combo Files-Local Combo","Combo Files-State Combo"]:
                docs = self.client.search(
                    collection_name=collection['file'],
                    query_vector=vector,
                    query_filter = Filter(
                        must = [
                            FieldCondition(
                                    key="state",
                                    match=MatchValue(
                                        value=state,
                                    ),
                            )
                        ]
                    )
                    ,
                    limit=limit

                )

                documents.extend([doc.payload['text']+"\n" for doc in docs])

            if collection["file"] in ["General Information","Combo Files-National Combo","Specialty"]:
                docs = self.client.search(
                    collection_name=collection['file'],
                    query_vector=vector,
                    limit=limit

                )

                documents.extend([doc.payload['text']+"\n" for doc in docs])

            if collection['file'] == "Specialty":
                docs = self.client.search(
                    collection_name=collection['file'],
                    query_vector=vector,
                    limit=limit,
                    query_filter = Filter(
                        must = [
                            FieldCondition(
                                    key="type",
                                    match=MatchValue(
                                        value=license_level,
                                    ),
                            )
                        ]
                    )
                   

                )

                documents.extend([doc.payload['text']+"\n" for doc in docs])


        return documents[:limit]
