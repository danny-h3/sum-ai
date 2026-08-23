import redis
from secrets import token_urlsafe
from app.core.config import settings

r = redis.Redis.from_url(settings.redis_url)

def gen_task_id(): 
    return token_urlsafe(16)

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
