from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.log import submit_log
from typing import List, Optional
from app.models.log import DailyLog
from datetime import date
import json
import os

router = APIRouter(prefix="/log", tags=["Daily Log"])

import uuid
from pathlib import Path

@router.post("/submit")
async def submit_daily_log(
    emp_id: str = Form(...),
    site_id: int = Form(...),
    weather: str = Form(...),
    work_done: str = Form(...),
    safety_note: str = Form(""),
    materials: str = Form("[]"),
    photos: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    materials_list = json.loads(materials)
    photos_paths = []

    upload_dir = Path("static/logs")
    upload_dir.mkdir(parents=True, exist_ok=True)

    for photo in photos:
        # FIX FOR WEB — filename can be null!
        original_filename = photo.filename or f"photo_{uuid.uuid4()}.jpg"
        file_ext = original_filename.split(".")[-1] if "." in original_filename else "jpg"
        filename = f"{uuid.uuid4()}.{file_ext.lower()}"
        file_path = upload_dir / filename
        
        with open(file_path, "wb") as f:
            content = await photo.read()
            f.write(content)
        
        photos_paths.append(f"/static/logs/{filename}")

    log = submit_log(db, emp_id, site_id, weather, work_done, safety_note, materials_list, photos_paths)
    return {"msg": "Log submitted", "log_id": log.id}

@router.get("/")
def get_logs(
    site_id: Optional[int] = None,
    emp_id: Optional[str] = None,
    date_str: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DailyLog)
    if site_id:
        query = query.filter(DailyLog.site_id == site_id)
    if emp_id:
        query = query.filter(DailyLog.emp_id == emp_id)
    if date_str:
        try:
            log_date = date.fromisoformat(date_str)
            query = query.filter(DailyLog.date == log_date)
        except:
            raise HTTPException(400, "Invalid date — use YYYY-MM-DD")
    logs = query.all()
    return [
        {
            "id": l.id,
            "emp_id": l.emp_id,
            "name": l.employee.name if l.employee else "Unknown",
            "profile_pic": l.employee.profile_pic if l.employee else "/static/default-avatar.png",
            "site_id": l.site_id,
            "site_name": l.site.name if l.site else "Unknown Site",
            "date": l.date.isoformat(),
            "weather": l.weather,
            "work_done": l.work_done,
            "safety_note": l.safety_note,
            "materials_used": l.materials_used,
            "photo_urls": l.photos,
            "photo_count": len(l.photos),
            "submitted_at": l.submitted_at.isoformat()
        } for l in logs
    ]