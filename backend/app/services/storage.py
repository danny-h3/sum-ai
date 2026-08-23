from minio import Minio, ServerError, S3Error, InvalidResponseError
from app.core.config import settings

minio_client = None
app_bucket_name = settings.minio_bucket_name

# creates and returns minio client 
def create_client(): 
    global minio_client
    if minio_client is None: 
        minio_client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key
        ) 
    return minio_client

# create a key for file
def create_obj_key(username: str, filename: str):
    return f"users/{username}/file/{filename}"

# create a bucket using given client + bucket_name then return status
def create_bucket(client: Minio):
    if client.bucket_exists(bucket_name=app_bucket_name):
        return {"msg": "exists"}

    try: 
        client.make_bucket()
    except ValueError as err:
        return {"msg": "invalid bucket name", "err": err}
    except S3Error as err: 
        return {"msg": "bucket exists", "err": err}
    except ServerError as err: 
        return {"msg": "unexpected server response", "err": err}
    except Exception as err:
        return {"msg": "unexpected error", "err": err}
    return {"msg": "success"}

# upload a file to the bucket, then return status
def upload_file(client: Minio, file_name: str, file: bytes, file_len: int):
    try:
        res = client.put_object(bucket_name=app_bucket_name, object_name=file_name, object=file, length=file_len)
    except S3Error as err:
        if err.code == "InvalidObjectName":
            return {"msg": f"bad object name, {file_name}", "err": err}
    except ServerError as err:
        return {"msg": f"server failed with code {err.status_code}", "err": err}
    except InvalidResponseError as err:
        return {"msg": f"invalid server response", "err": err}
    except Exception as err: 
        return {"msg": "unexpected error", "err": err} 
    if res:
        return {"msg": "success"}

# delete a file
def delete_file(client: Minio, obj_name: str):
    try: 
        client.remove_object(bucket_name=app_bucket_name, object_name=obj_name)
    except S3Error as err:
        if err.code == "InvalidObjectName":
            return {"msg": f"bad object name, {obj_name}", "err": err}
        if err.code == "NoSuchKey":
            return { "msg": f"bad key, {obj_name}", "err": err}
    except ServerError as err:
        return {"msg": f"server failed with code {err.status_code}", "err": err}
    except InvalidResponseError as err:
        return {"msg": f"invalid server response", "err": err}
    except Exception as err: 
        return {"msg": "unexpected error", "err": err} 
    return {"msg": "success"}

# grab a file
def get_file(client: Minio, obj_name: str):
    try: 
        res = client.get_object(bucket_name=app_bucket_name, object_name=obj_name)
    except S3Error as err:
        if err.code == "InvalidObjectName":
            return {"msg": f"bad object name, {obj_name}", "err": err}
        if err.code == "NoSuchKey":
            return {"msg": f"bad key, {obj_name}", "err": err}
    except ServerError as err:
        return {"msg": f"server failed with code {err.status_code}", "err": err}
    except InvalidResponseError as err:
        return {"msg": f"invalid server response", "err": err}
    except Exception as err: 
        return {"msg": "unexpected error", "err": err} 
    else:
        return {"msg": "success", "res": res.read()}
    finally: 
        if res: 
            res.close()
            res.release_conn()
        

