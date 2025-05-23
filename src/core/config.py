from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    upload_dir: str = "uploaded_files"
    title: str = "Plagiarism Detector API"
    version: str = "1.0.0"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
