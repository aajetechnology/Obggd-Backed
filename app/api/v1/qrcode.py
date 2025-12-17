from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.qrcode import create_qr
from app.models.qrcode import QRCode
from datetime import date
from pydantic import BaseModel
import qrcode
from io import BytesIO

router = APIRouter(prefix="/qrcode", tags=["QR"])

class QRRequest(BaseModel):
    site_name: str
    location: str
    project_start: date
    project_end: date

@router.post("/")
def make(request: QRRequest, db: Session = Depends(get_db)):
    qr = create_qr(db, request.site_name, request.location, request.project_start, request.project_end)
    return {
        "message": "QR created",
        "site_id": qr.id,
        "qr_data": qr.qr_data
    }

@router.get("/{site_name}/image")
def image(site_name: str, db: Session = Depends(get_db)):
    qr = db.query(QRCode).filter(QRCode.site_name == site_name).first()
    if not qr:
        raise HTTPException(404, "QR not found")
    img = qrcode.make(qr.qr_data)
    buf = BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@router.get("/all")
def get_all_sites(db: Session = Depends(get_db)):
    sites = db.query(QRCode).all()
    return [{"id": s.id, "site_name": s.site_name, "location": s.location, "project_start": s.project_start.isoformat(), "project_end": s.project_end.isoformat()} for s in sites]