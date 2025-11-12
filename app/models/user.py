from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="worker")
    department = Column(String, default="General")  # NEW
    employee_id = Column(String, unique=True)
    profile_pic = Column(String, default="default.jpg")
    created_at = Column(DateTime, default=datetime.utcnow)