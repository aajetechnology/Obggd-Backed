from sqlalchemy.orm import Session
from app.models.site import Site

def create_site(db: Session, name: str, location: str):
    qr_text = f"OBGGD:SITE:{name}|LOC:{location}|ID:NEW"
    db_site = Site(name=name, location=location, qr_code=qr_text)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site