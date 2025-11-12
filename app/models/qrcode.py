from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class QRCode(Base):
    __tablename__ = "qrcodes"
    id = Column(Integer, primary_key=True)
    site_name = Column(String, unique=True)
    location = Column(String)          
    project_start = Column(Date)
    project_end = Column(Date)
    qr_data = Column(String)