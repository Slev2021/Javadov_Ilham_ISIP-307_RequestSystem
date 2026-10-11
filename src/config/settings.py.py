import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MODE: str = os.getenv("MODE", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    DB_PATH: str = os.getenv("DB_PATH", "requestsystem.db")

    API_TITLE: str = os.getenv("API_TITLE", "RequestSystem API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")


settings = Settings()