from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from worker import worker
import json

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Hello World" }

# Take a input + file from client
@app.post("/upload/")
async def upload_package(
    input: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    if not input and not file:
        raise HTTPException(status_code=400, detail="Input and File not found")
    
    # temp, used for testing different prompts 
    with open('test_prompts.json', 'r', encoding="utf-8") as f:
        data = json.load(f)

    # pass contents to worker
    file_bytes = await file.read() if file else None
    worker.delay(input, file_bytes, "\n".join(data["sample_1"]) )

    return {"msg": "[SUCCESS]: worker started" }

@app.post("/resummarize/")
def resummarize():
    return