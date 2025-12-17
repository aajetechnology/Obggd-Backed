from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date

class DailyAttendance(Base):
    __tablename__ = "daily_attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.emp_code"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    date = Column(Date, default=date.today, nullable=False)
    clock_in = Column(DateTime)
    clock_out = Column(DateTime)
    status = Column(String, default="absent")

    employee = relationship("Employee", back_populates="attendance_records")
    site = relationship("Site", back_populates="attendance_records")