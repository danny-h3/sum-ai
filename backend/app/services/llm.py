import httpx
import json
from app.core.config import settings

def llm_call(user_content: str): 
    sys_msg =  ""
    with open('prompts.json', 'r', encoding="utf-8") as f:
        data = json.load(f)

    if settings.mode == "demo": 
        sys_msg = data.join("\n".join(data["demo"]))
    else: 
        sys_msg = data.join("\n".join(data["personal"]))

    llm_endpoint = settings.ai_model_url
    if not llm_endpoint:
        return 0
    
    llm_endpoint += "/v1/chat/completions"

    msg = { 
        "model": settings.ai_model_name,
        "messages": [
            {"role": "system", "content": sys_msg}, 
            {"role": "user", "content": user_content}
        ]}
    
    try: 
        res = httpx.post(llm_endpoint, json=msg, timeout=300)
        data = res.json()
    except httpx.HTTPError as exc: 
        return {"error": f"HTTP Exception for {exc.request.url} - {exc}"}
    
    return data["choices"][0]["message"]["content"]