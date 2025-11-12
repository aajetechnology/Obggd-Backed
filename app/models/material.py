from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class MaterialRequest(Base):
    __tablename__ = "material_requests"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey("users.employee_id"))
    material = Column(String)
    quantity = Column(String)
    notes = Column(String)
    status = Column(String, default="Requested")  # Requested → Approved → In Transit → Delivered
    eta = Column(String, default="45 min")
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_by = Column(String, nullable=True)
    delivered_at = Column(DateTime, nullable=True)