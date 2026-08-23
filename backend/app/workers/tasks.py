import logging 
import pymupdf

from celery import Celery
from app.services.llm import llm_call
from app.core.security import settings

import app.services.storage as storage
import backend.app.db.crud as crud
import app.services.cache as rc

# Each worker get's their own db session client
logger = logging.getLogger("[celery_worker]")

def textExtractor( key: str):
    if not key: 
        logger.error("[%s] given an emtpy search key.", "textExtractor") 
        return

    # figure out way to pass bucket/ client in here // this can be own function
    file = storage.get_file("client", key)
    if not file:
        return ""
    
    file_bytes = file.read()
    # set to pdf for now, maybe support more files in future
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    content = ""
    for page in doc:
        text = page.get_text()
        if not text:
            tp = page.get_textpage_ocr()
            text = page.get_text(textpage=tp)
        content += text + "\n"
    return content
         
# Add redis later
app = Celery('llm_worker', broker=settings.redis_url)

"""
    worker takes a package, processes it, and passes a prompt to LLM.
"""
@app.task
def worker( task_id: str, key_dict: dict):
    if not key_dict:
        rc.xadd_stream(task_id,"error", "Something went wrong...")
        logger.error("empty parameters given, stopping ...") 
        return 
    
    minio_client = storage.create_client()
    psql_engine, psql_session = crud.create_psql()
    

    rc.xadd_stream( task_id, "start", "Received task")
    logger.info("received input(s) and files(s) starting workflow ...")

    # process input
    if "input" in key_dict:
        rc.xadd_stream(task_id, "progress", "Summarizing text ...")
        logger.info("workong on summarizing input ...")
        result = llm_call(key_dict["input"])
        crud.summary_store(db=psql_session(), summary_text=result, input_id=key_dict["input"])
        if "error" in result: 
            rc.xadd_stream(task_id, "error", "server error")
            logger.info(f"error calling llm, llm_call returned: {result["error"]}")
            return 
        # we want to remove this so we dont interfere with file text extraction below
        del key_dict["input"]

    # process key_dict
    if key_dict:
        rc.xadd_stream( task_id, "progress", "Processing files")
        logger.info("extracting file text from file bytes ...")

        for i, (file_key, file_id) in enumerate(key_dict.items()): 
            rc.xadd_stream( task_id, "progress", f"Summarizing file {i}")
            logger.info(f"working on file [{i + 1}] ...")

            file_text = textExtractor(file_key, minio_client) + "\n-------"
            result = llm_call(file_text)
            if "error" in result: 
                rc.xadd_stream(task_id, "error", "server error")
                logger.info(f"error calling llm, llm_call returned: {result["error"]}")
                return 
            crud.summary_store(db=psql_session(), summary_text=result, file_id=file_id,)

    rc.xadd_stream( task_id, "complete", "Returning")
    logger.info("task complete, cleaning up ...")
    psql_engine.dispose() 
    return