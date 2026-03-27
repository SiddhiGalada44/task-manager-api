from sqlalchemy import create_engine ,Column,Integer,String, Boolean , ForeignKey
from sqlalchemy.orm import DeclarativeBase , relationship
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

class Base(DeclarativeBase):
    pass    

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement =True)
    email =Column(String, unique=True , nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__="tasks"
    id = Column(Integer, primary_key=True, autoincrement =True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")

def init_db():
    Base.metadata.create_all(engine)
    