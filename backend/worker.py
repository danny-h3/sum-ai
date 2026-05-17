from celery import Celery
from llm_caller import llm_call
import logging 
import pymupdf
import redis_client as rc

logger = logging.getLogger("[Celery_Worker]")

def textExtractor( fileBytes: bytes ):
    if not fileBytes: 
        logger.error("Given a empty document ... ") 
        return

    # leave file type param empty to support multiple files
    doc = pymupdf.open(stream=fileBytes, filetype="pdf")
    content = ""
    for page in doc:
        text = page.get_text()
        if not text:
            tp = page.get_textpage_ocr()
            text = page.get_text(textpage=tp)
        content += text + "\n"
    return content
         
# Add redis later
app = Celery('worker', broker='redis://localhost:6379/0')

"""
    worker takes a package, processes it, and passes a prompt to LLM.
"""
@app.task
def worker( task_id: str, user_input: str, file_bytes_arr: bytes, sys_instr: str ):
    if not user_input and not fileBytes:
        logger.error("Empty parameters given, stopping ... ") 
        return 
    
    rc.xadd_stream( task_id, "start", "Received files")
    logger.info("Received instruction(s) and files(s) starting workflow ... ")

    rc.xadd_stream( task_id, "progress", "Constructing instructions")
    instr, text = "", ""
    if user_input: 
        instr = user_input
    if file_bytes_arr: 
        rc.xadd_stream( task_id, "progress", "Processing files")
        logger.info("Extracting file text from file bytes ... ")
        for i, fileBytes in enumerate(file_bytes_arr): 
            logger.info(f"Working on file [{i + 1}] ... ")
            text += textExtractor(fileBytes) + "\n\n-------\n"

    rc.xadd_stream( task_id, "progress", "Constructing model prompt")
    logger.info("Constructing msg for model ... ")
    usr_msg = f"{instr}\n\n-------\n{text}"

    rc.xadd_stream( task_id, "progress", "Waiting for model response")
    logger.info("Calling model ... ")
    result = llm_call(sysMsg=sys_instr, usrMsg=usr_msg)
    
    # Store model response to PSQL 

    rc.xadd_stream( task_id, "complete", "Returning")

    logger.info("Complete!")
    return