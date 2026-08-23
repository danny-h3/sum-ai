from fastapi import APIRouter, HTTPException
from db import crud

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# upload a file containing relevant information about the admin
# 
@router.post("/upload/")
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

