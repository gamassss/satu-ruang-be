from fastapi import FastAPI
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.chat import router as chat_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Satu Ruang!"}

