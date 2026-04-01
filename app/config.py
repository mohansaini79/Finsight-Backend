import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Finance Dashboard Backend")
    mongo_uri: str = os.getenv("MONGO_URI", "").strip().strip('"').strip("'")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME", "exam_db")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "").strip()
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


settings = Settings()
