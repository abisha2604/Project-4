from sqlalchemy.orm import Session
from models.chat_schema import Chat
from database.get_db import get_db
from groq import Groq
from fastapi import UploadFile,File
import os
import shutil
import mimetypes
from fastapi.responses import FileResponse


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_history(db):
    return db.query(Chat).all()

def create_chat(db:Session,question:str):

    history = create_history(db)

    messages = []

    for chat in history:
        messages.append({"role": "user", "content": chat.question})
        messages.append({"role": "system", "content": chat.question})

    messages.append({"role": "user", "content": question})

    client=Groq(api_key=" API KEY ")
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


def upload_file(db:Session,question:str,file:UploadFile):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as b:
        shutil.copyfileobj(file.file, b)

    with open(file_path, "r") as f:
        content = f.read()

    client=Groq(api_key=" API KEY")
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=2,
        messages=[{"role":"user","content":f"Answer the {question}using{content}"}],
        max_tokens=200

    )
    response = response.choices[0].message.content

    q = Chat(question=f"Summerize file: {file.filename}",answer=response)
    
    db.add(q)
    db.commit()
    db.refresh(q)


    return {"user": question,"bot": response}

    



    






