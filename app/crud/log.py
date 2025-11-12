from sqlalchemy.orm import Session
from app.models.log import DailyLog
from datetime import date

def submit_log(
    db: Session,
    emp_id: str,
    site_id: int,
    weather: str,
    work_done: str,
    safety_note: str,
    materials: list,
    photos: list
):

    if material is None:
        materials = []
    if photos is None:
        photos = []

    log = DailyLog(
        employee_id=emp_id,
        site_id=site_id,
        date=date.today(),
        weather=weather,
        work_done=work_done,
        safety_note=safety_note,
        materials_used=materials,
        photos=len(photos),
        submit_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log