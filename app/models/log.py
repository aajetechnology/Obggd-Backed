from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, JSON
from app.core.database import Base
from datetime import datetime

class DailyLog(Base):
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey("users.employee_id"))
    site_id = Column(Integer, ForeignKey("sites.id"))
    date = Column(Date)
    weather = Column(String)
    work_done = Column(String)
    safety_note = Column(String)
    materials_used = Column(JSON)  # [{"name": "Cement", "qty": "50"}]
    photos = Column(JSON)         # ["url1", "url2"]
    submitted_at = Column(DateTime, default=datetime.utcnow)