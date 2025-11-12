from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    location = Column(String)
    head_id = Column(String, ForeignKey("users.employee_id"))  # Site Head