from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date, datetime

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String, ForeignKey("employees.emp_code"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    date = Column(Date, default=date.today, nullable=False)
    weather = Column(String, nullable=False)
    work_done = Column(String, nullable=False)
    safety_note = Column(String, default="")
    materials_used = Column(JSON, default=list)
    photos = Column(JSON, default=list)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="logs")
    site = relationship("Site", back_populates="logs")