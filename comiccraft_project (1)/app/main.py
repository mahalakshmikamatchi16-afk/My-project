import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ComicCraft - AI Comic Story Creator Portal")

os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)
os.makedirs("static/fonts", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

from app.routes import router
app.include_router(router)
