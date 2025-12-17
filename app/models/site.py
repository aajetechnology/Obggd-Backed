from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    qr_code = Column(String, unique=True, nullable=False)

    # Relationships
    assignments = relationship("SiteEmployeeAssignment", back_populates="site")
    logs = relationship("DailyLog", back_populates="site")
    attendance_records = relationship("DailyAttendance", back_populates="site")