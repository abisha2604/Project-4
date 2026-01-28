from pydantic import BaseModel

class ResponseModel(BaseModel):
    question:str
    answer:str
    
class RequestModel(BaseModel):
    question:str

class ImageRequest(BaseModel):
    prompt:str
