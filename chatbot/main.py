from fastapi import FastAPI
from routes.chat_route import router
import os


app= FastAPI(title="ChatBot")

app.include_router(router)





