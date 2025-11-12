from sqlalchemy.orm import Session
from app.models.qrcode import QRCode
from datetime import date

def create_qr(
    db: Session,
    site_name: str,
    location: str,
    project_start: date,
    project_end: date
):
    qr_data = (
        f"OBGGD:SITE:{site_name}"
        f"|LOC:{location}"
        f"|START:{project_start}"
        f"|END:{project_end}"
    )
    
    qr = QRCode(
        site_name=site_name,
        location=location,
        project_start=project_start,
        project_end=project_end,
        qr_data=qr_data
    )
    
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return qr