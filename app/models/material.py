from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import func

class MaterialRequest(Base):
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, ForeignKey("employees.emp_code"), nullable=False, index=True)
    material = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    notes = Column(Text)
    status = Column(String, default="pending", index=True)
    eta = Column(Integer)
    requested_at = Column(DateTime, server_default=func.now())
    approved_at = Column(DateTime)
    approved_by = Column(String)
    declined_at = Column(DateTime)
    declined_by = Column(String)
    decline_reason = Column(Text)
    delivered_at = Column(DateTime)

    
    employee = relationship("Employee", back_populates="material_requests")