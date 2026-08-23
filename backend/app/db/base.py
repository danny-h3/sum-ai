from sqlalchemy.orm import Session

from backend.app.db import crud
from app.services import storage

minio_client = storage.create_client()
psql_engine, psql_session = crud.create_psql()

def get_db():
    with psql_session() as session:
        yield session


    