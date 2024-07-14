from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGODB_URL: str
    DATABASE_NAME: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
