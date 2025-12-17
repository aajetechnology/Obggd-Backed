from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class QRCode(Base):
    __tablename__ = "qrcodes"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    project_start = Column(Date, nullable=False)
    project_end = Column(Date, nullable=False)
    qr_data = Column(String, nullable=False)