from fastapi import FastAPI, UploadFile, Form, File, HTTPException, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from app.services import storage
from backend.app.workers.tasks import worker
from backend.app.db import crud
from app.services import cache

# load db clients on start up
@asynccontextmanager
async def lifespan(app: FastAPI):
    minio_client = storage.create_client()
    psql_engine, psql_session = crud.create_psql()
    app.state.minio_client = minio_client
    app.state.psql_engine = psql_engine
    app.state.psql_session = psql_session

    yield

    app.state.psql_engine.dispose()

def get_db():
    with app.state.psql_session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return { "msg": "Hello World" }

# Take a input + file(s) from client, return a redis task id 
# ADD: authenticate client call
@app.post("/upload/")
async def upload_package(
    db: SessionDep,
    input: str | None = Form(None),
    files: list[UploadFile] | None = File(None),
):
    # right now endpoint doesn't verify user, implement this later
    if not input and not files:
        raise HTTPException(status_code=400, detail="Input and File not found")

    key_id_dict = {}    
    if input is not None: 
        input_id = crud.input_store(db, 0000, input)
        key_id_dict["input"] = input_id

    if files is not None:
        for i, file in enumerate(files):
            if i >= 3: 
                raise HTTPException(status_code=501, detail="Too many files")
            
            file_key = storage.create_obj_key("[username]", filename=file.filename)
            status = storage.upload_file(app.state.minio_client,  file.filename, file.file, file.size)
            if status["msg"] != "success": 
                print(f"[Error] minio returned: {status["msg"]}, err: {status["err"]}")

            # store in psql next
            file_id = crud.file_store(db, "[username]", filename=file.filename, obj_key=file_key)
            if not file_id: 
                print(f"[Error] storing file {file.filename} to DB")
                break
            
            key_id_dict[file_key] = file_id
    
    # generate redis task id
    r_task_id = cache.gen_task_id()

    # start worker
    worker.delay(r_task_id, key_id_dict)
    return {"msg": "upload sucessful, worker started", "task_id": r_task_id}

@app.get("/stream/")
async def get_stream():
    pass 

@app.post("/resummarize/")
def resummarize():
    pass