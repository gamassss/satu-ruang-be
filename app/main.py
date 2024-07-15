from fastapi import FastAPI
from app.core import settings
from app.db import connect_to_mongo, close_mongo_connection
from app.api import chat
from app.api import websocket as ws

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(ws.router, tags=["websocket"])

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Satu Ruang!"}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

static_dir = os.path.join(os.path.dirname(__file__), 'static')

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get():
    return FileResponse(os.path.join(static_dir, 'index.html'))

