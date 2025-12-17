from sqlalchemy.orm import Session
from app.models.log import DailyLog
from app.models.employee import Employee
from datetime import date, datetime

def submit_log(
    db: Session,
    emp_id: str,
    site_id: int,
    weather: str,
    work_done: str,
    safety_note: str = "",
    materials: list = None,
    photos_arrays: list = None
):
    employee = db.query(Employee).filter(Employee.emp_code == emp_id).first()
    if not employee:
        raise ValueError(f"Employee {emp_id} not found")

    log = DailyLog(
        emp_id=emp_id,
        site_id=site_id,
        weather=weather,
        work_done=work_done,
        safety_note=safety_note or "",
        materials_used=materials or [],
        photos=photos_arrays or [],
        submitted_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log