from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey, LargeBinary
from database.db import engine

Base = declarative_base()

class Chat(Base):
    __tablename__ ='chat'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    image_id = Column(String, primary_key=True, index=True)
    prompt = Column(String)
    image_data = Column(LargeBinary)
    
Base.metadata.create_all(engine)