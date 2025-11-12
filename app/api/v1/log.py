from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.log import DailyLog
from app.crud.log import submit_log

router = APIRouter(prefix="/log", tags=["Daily Log"])

@router.post("/submit")
def submit_daily_log(
    emp_id: str,
    site_id: int,
    weather: str,
    work_done: str,
    safety_note: str = "",
    materials: list = None,
    photos: list = None,
    db: Session = Depends(get_db)
):
    if materials is None: materials = []
    if photos is None: phone = []


    log = submit_log(db, emp_id, site_id, weather, work_done, safety_note, materials, photos)
    return {
        "msg": "Daily Log Submitted!",
        "log_id": log.id,
        "date": str(log.date),
        "worker": emp_id,
        "weather": weather,
        "materials_used": len(materials),
        "photos": len(photos)



    }

@router.get("/all")
def get_all_logs(date: str = None, db: Session = Depends(get_db)):
    query = db.query(DailyLog)
    if date:
        query = query.filter(DailyLog.date == date)
    logs = query.order_by(DailyLog.submitted_at.desc()).all()
    
    return [
        {
            "id": l.id,
            "employee_id": l.employee_id,
            "site_id": l.site_id,
            "date": l.date,
            "weather": l.weather,
            "work_done": l.work_done,
            "photo_count": l.photo_count
        }
        for l in logs
    ]