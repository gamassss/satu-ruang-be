from fastapi import FastAPI
from app.core import settings
from app.db import connect_to_mongo, close_mongo_connection
from app.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Satu Ruang!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

