from fastapi import APIRouter
from app.api.chat import router as chat_router
from app.api.websocket import router as websocket_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(websocket_router, prefix="/websocket", tags=["websocket"])
