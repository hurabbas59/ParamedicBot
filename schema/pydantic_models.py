from pydantic import BaseModel

class UploadResponse(BaseModel):
    status: str
    message: str

class QueryRequest(BaseModel):
    query: str
    license_level: str
    state: str

class QueryResponse(BaseModel):
    response: str