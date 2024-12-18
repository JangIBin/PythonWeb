from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    __table_args__ = {'extend_existing': True}

from sqlalchemy import Column, Integer, String, Date, Text
from app.database.connection import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String, nullable=False)
    task_name = Column(String, nullable=False)
    due_date = Column(Date, nullable=False)
    task_content = Column(Text, nullable=True)
    remarks = Column(Text)

    __table_args__ = {'extend_existing': True}