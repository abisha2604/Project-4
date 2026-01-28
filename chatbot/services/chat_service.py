from sqlalchemy.orm import Session
from models.chat_schema import Chat, GeneratedImage
from database.get_db import get_db
from groq import Groq
from fastapi import UploadFile,File
import os
import shutil
import mimetypes
from fastapi.responses import FileResponse
import requests
import uuid
from pypdf import PdfReader

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

API_KEY = " "

def create_history(db):
    return db.query(Chat).all()

def create_chat(db:Session,question:str):

    history = create_history(db)

    messages = []

    for chat in history:
        messages.append({"role": "user", "content": chat.question})
        messages.append({"role": "system", "content": chat.question})

    messages.append({"role": "user", "content": question})

    client=Groq(api_key= API_KEY)
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=2,
        messages=messages,
        max_tokens=100

    )
    response = response.choices[0].message.content
   
    chatbot = Chat(question=question,answer=response)
    db.add(chatbot)
    db.commit()
    db.refresh(chatbot)
    return{"User":question,"Bot":response}
   
def clear_history(db:Session):
    db.query(Chat).delete()
    db.commit()
    return {"message": "Chat history cleared"}


def upload_file(db: Session,question: str,file: UploadFile):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as b:
        shutil.copyfileobj(file.file, b)

    reader = PdfReader(file_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text() or ""


    client=Groq(api_key= API_KEY)
    prompt = f"""
        You are a document-based assistant.
        Answer only using the information in the DOCUMENT below.
        DOCUMENT:
        {content}

        QUESTION:
        {question}
        """


    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=2,
        messages=[{"role":"user","content":prompt}],
        max_tokens=200

    )
    response = response.choices[0].message.content

    q = Chat(question=f"Summerize file: {file.filename}",answer=response)
    
    db.add(q)
    db.commit()
    db.refresh(q)


    return {"user": question,"bot": response}

def generate_image_service(prompt: str, db: Session) -> bytes:

    HF_API_KEY = " API KEY"
    HF_URL = " URL "

    headers = {"Authorization": f"Bearer {HF_API_KEY}","Content-Type": "application/json"}
    response = requests.post(HF_URL,headers=headers,json={"inputs": prompt})

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Image generation failed")


    image_bytes = response.content
    image_entry = GeneratedImage(
        image_id=str(uuid.uuid4()),
        prompt=prompt,
        image_data=image_bytes)
    db.add(image_entry)
    db.commit()

    return image_bytes