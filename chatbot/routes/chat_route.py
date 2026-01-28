from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.get_db import get_db
from models.schema import ResponseModel, RequestModel, ImageRequest
from services.chat_service import create_chat,create_history,clear_history,upload_file,generate_image_service
from fastapi import UploadFile,File,Form
from typing import List
from fastapi import Response

router = APIRouter()

@router.post("/chat")
def user_question(data:RequestModel,db:Session=Depends(get_db)):
    return create_chat(db,data.question)

@router.get("/history",response_model=list[ResponseModel])
def get_all_history(db:Session=Depends(get_db)):
    return create_history(db)

@router.delete("/clear-history")
def delete_history(db:Session=Depends(get_db)):
    return clear_history(db)

@router.post("/upload-file")
def upload_file_data(question:str=Form(...),file:UploadFile=File(...),db:Session=Depends(get_db)):
    return upload_file(db,question,file)

@router.post("/generate-image")
def generate_image(data:ImageRequest,db: Session = Depends(get_db)):
    image_bytes = generate_image_service(data.prompt,db)
    return Response(content=image_bytes,media_type="image/png")