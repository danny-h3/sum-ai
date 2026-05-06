import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env.local")


def llm_call(sysMsg: str, usrMsg: str): 

    llm_endpoint = os.getenv("LLM_ENDPOINT")
    if not llm_endpoint:
        return 0
    
    llm_endpoint += "/v1/chat/completions"

    msg = { 
        "model": "qwen2.5-3b-instruct-q4_k_m.gguf",
        "messages": [
            {"role": "system", "content": sysMsg}, 
            {"role": "user", "content": usrMsg}
        ]}
    res = httpx.post( llm_endpoint, json=msg, timeout=300)
    data = res.json()

    return data["choices"][0]["message"]["content"]