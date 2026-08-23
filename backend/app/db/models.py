from sqlalchemy import Integer, String, BINARY, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from typing import List

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id:       Mapped[int]   = mapped_column(Integer, primary_key=True)
    username: Mapped[str]   = mapped_column(String, nullable=False, unique=True)
    email:    Mapped[str]   = mapped_column(String, nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(BINARY, nullable=False)

    files:     Mapped[List["UserFile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    inputs:   Mapped[List["UserInput"]] = relationship(back_populates="user", cascade="all, delete-orphan")

# Note: files aren't stored in psql, stored in minio instead
class UserFile(Base): 
    __tablename__ = "files"

    id:         Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:    Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    file_name:   Mapped[str] = mapped_column(String)
    minio_key:  Mapped[str] = mapped_column(String, unique=True)

    user:       Mapped["User"] = relationship(back_populates="files")
    summary:    Mapped["Summary"] = relationship(back_populates="file", cascade="all, delete-orphan") #one summmary for now more in future

class UserInput(Base):
    __tablename__ = "inputs"
    id:        Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:   Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    text:      Mapped[str] = mapped_column(String)

    user:      Mapped["User"] = relationship(back_populates="inputs")
    summary:   Mapped["Summary"] = relationship(back_populates="input", cascade="all, delete-orphan")

# since summaries aren't too long store in psql
class Summary(Base): 
    __tablename__ = "summaries"

    id:       Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id:   Mapped[int] = mapped_column(Integer, ForeignKey("files.id"), nullable=True)
    input_id: Mapped[int] = mapped_column(Integer, ForeignKey("inputs.id"), nullable=True)
    text:     Mapped[str] = mapped_column(String)

    file:      Mapped["UserFile"] = relationship(back_populates="summary")
    input:    Mapped["UserInput"] = relationship(back_populates="summary")