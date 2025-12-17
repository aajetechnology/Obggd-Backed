from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class SiteEmployeeAssignment(Base):
    __tablename__ = "site_employee_assignments"

    site_id = Column(Integer, ForeignKey("sites.id"), primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    site = relationship("Site", back_populates="assignments")
    employee = relationship("Employee", back_populates="assignments")