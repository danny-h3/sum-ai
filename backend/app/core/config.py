import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    mode: str
    redis_url: str
    psql_url: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    ai_model_url: str
    ai_model_name: str
    secret: str
    access_expire: int

def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable {name}")
    return value

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env.local"

load_dotenv(dotenv_path)

settings = Settings(
    mode                = _required("APP_MODE"),
    redis_url           = _required("REDIS_URL"),
    psql_url            = _required("PSQL_URL"),
    minio_endpoint      = _required("MINIO_ENDPOINT"),
    minio_access_key    = _required("MINIO_ACCESS_KEY"),
    minio_secret_key    = _required("MINIO_SECRET_KEY"),
    minio_bucket_name   = _required("MINIO_BUCKET_NAME"),
    ai_model_url        = _required("LLM_ENDPOINT"),
    ai_model_name       = _required("LLM_NAME"),
    secret              = _required("ACCESS_SECRET_KEY"),
    access_expire       = int(_required("ACCESS_TOKEN_EXPIRE_MINS")),
    refresh_expire      = int(_required("REFRESH_TOKEN_EXPIRE_MINS"))
)
