import redis
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env.local")

REDIS_URL =  os.getenv("REDIS")

r = redis.Redis.from_url( REDIS_URL )

# update redis stream, return True on success, False otherwise
def xadd_stream(task_id: str, event: str, data: str): 
    res = r.xadd( task_id, { "event": event, "data": data } )
    if res: 
        return True
    return False

# delete a stream and return True on success, False otherwise
def del_stream(task_id: str): 
    r.delete( task_id )
    if not r.xlen( task_id ): 
        return True
    return False
