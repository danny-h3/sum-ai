from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker, joinedload, subqueryload
from backend.app.db.models.models import Base, User, UserFile, UserInput, Summary
from app.core.config import settings

# creates psql using schema.py
def create_psql(): 
    engine = create_engine(settings.psql_url)
    Base.metadata.create_all(engine)
    local_session = sessionmaker(engine)
    return engine, local_session

# ---- stores ---- #
# store user account info
def user_store(db: Session, username: str, email: str, password: bytes):
   user = User(
       username=username, 
       email=email,
       password=password
   )
   db.add(user)
   db.commit()
   db.refresh(user)
   return user.id

# store user file upload
def file_store(db: Session, username: str, filename: str, obj_key: str ):
    stmt = select(User.id).where(username==username) 
    user_id = db.scalar(stmt)

    file = UserFile(
        user_id=user_id,
        file_name=filename,
        minio_key=obj_key, 
    )

    db.add(file)
    db.commit()
    db.refresh(file)
    return file.id

# store user input upload
def input_store(db: Session, user_id: int, input_text: str):
    user_input = UserInput(
        user_id=user_id,
        text=input_text
    )

    db.add(user_input)
    db.commit()
    db.refresh(user_input)
    return user_input.id

# store user summary upload
def summary_store(db: Session, summary_text: str, file_id: int=0, input_id: int=0):
    if file_id != 0: 
        summary = Summary(
            file_id=file_id,
            text=summary_text
        )
    elif input_id != 0:
        summary = Summary(
            input_id=input_id,
            text=summary_text
        )
    
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary.id

# ---- getters ---- #
# get everything about a user 
def get_everything(db: Session, username: str): 
    stmt = select(User).options(
        joinedload(User.files).subqueryload(UserFile.summary),
        joinedload(User.inputs).subqueryload(UserInput.summary) # erm is this correct? 
    ).filter_by(username=username)
    obj = db.scalar(stmt)
    return obj

# get user account info through username
def get_user_by_username(db: Session, username: str):
    stmt = select(User).filter_by(username=username)
    obj = db.scalar(stmt)
    return obj

# get user account info through email
def get_user_by_email(db: Session, email:str):
    stmt = select(User).filter_by(email=email)
    obj = db.scalar(stmt)
    return obj

# get a specific file from the user
def get_file(db: Session, file_id: str):
    stmt = select(UserFile).filter_by(id=file_id)
    obj = db.scalar(stmt)
    return obj

def get_input(db: Session, user_id: int): 
    stmt = select(UserInput).filter_by(user_id=user_id)
    obj = db.scalar(stmt)
    return obj

def get_summary(db: Session, file_id: int):
    stmt = select(Summary).filter_by(file_id=file_id)
    obj = db.scalar(stmt)
    return obj

# ---- delete ---- #
# remove user, cascades and removes everything else
def del_user(db:Session, username: str):
    stmt = select(User).filter_by(username=username)
    obj = db.scalar(stmt)
    if obj:
        db.delete(obj)
        db.commit()
    

# remove file, cascades and removes corresponding summary as well
def del_file(db: Session, filename: str):
    stmt = select(UserFile).filter_by(file_name=filename)
    obj = db.scalar(stmt)
    if obj: 
        db.delete(obj)
        db.commit()

# remove user input
def del_input(db: Session, user_id: str): 
    stmt = select(UserInput).filter_by(user_id=user_id)
    obj = db.scalar(stmt)
    if obj:
        db.delete(obj)
        db.commit()

# remove summary
def del_summary(db: Session, file_id: int):
    stmt = select(Summary).filter_by(file_id=file_id)
    obj = db.scalar(stmt)
    if obj: 
        db.delete(obj)
        db.commit()
        
