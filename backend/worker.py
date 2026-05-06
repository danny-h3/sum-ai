from celery import Celery
from llm_caller import llm_call
import logging 
import pymupdf

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
def worker( userInput: str, fileBytes: bytes, sysInstr: str ):
    if not userInput and not fileBytes:
        logger.error("Empty parameters given, stopping ... ") 
        return 
    
    logger.info("Received instruction(s) and files(s) starting workflow ... ")

    instr, text = "", ""
    if userInput: 
        instr = userInput
    if fileBytes: 
        logger.info("Extracting file text from package ... ")
        text = textExtractor(fileBytes)        

    usr_msg = f"{instr}\n\n-------\n{text}"

    logger.info("Calling model ... ")

    result = llm_call(sysMsg=sysInstr, usrMsg=usr_msg)
    logger.info("Model returned: ")
    logger.info(result)

    return