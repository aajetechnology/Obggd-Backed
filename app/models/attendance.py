from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from app.core.database import Base
from datetime import datetime

class WorkerSiteAssignment(Base):
    __tablename__ = "worker_assignments"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey("users.employee_id"))
    site_id = Column(Integer, ForeignKey("sites.id"))
    assigned_at = Column(DateTime, default=datetime.utcnow)

class DailyAttendance(Base):
    __tablename__ = "daily_attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey("users.employee_id"))
    site_id = Column(Integer, ForeignKey("sites.id"))
    date = Column(Date)
    clock_in = Column(DateTime, nullable=True)
    clock_out = Column(DateTime, nullable=True)
    status = Column(String, default="absent")  # present / absent