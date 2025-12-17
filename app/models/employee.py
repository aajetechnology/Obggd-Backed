# app/models/employee.py — FINAL VERSION (WORKS WITH EMAIL + PHONE LOGIN)
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, unique=True, index=True, nullable=False)  # e.g. OBGGD-001
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)  # e.g. 08012345678
    email = Column(String, unique=True, index=True, nullable=True)     # ← CRITICAL: ADD THIS
    department = Column(String, default="General")
    role = Column(String, default="worker")
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_pic = Column(String, default="/static/default-avatar.png")

    # Relationships
    attendance_records = relationship("DailyAttendance", back_populates="employee")
    material_requests = relationship("MaterialRequest", back_populates="employee")
    assignments = relationship("SiteEmployeeAssignment", back_populates="employee")
    logs = relationship("DailyLog", back_populates="employee", cascade="all, delete-orphan")