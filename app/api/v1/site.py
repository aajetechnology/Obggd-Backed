# app/api/v1/site.py — FINAL ETERNAL VERSION (DEC 2025)
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.site import create_site
from app.models.site import Site
from app.models.site_assignment import SiteEmployeeAssignment
from app.models.employee import Employee
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO

router = APIRouter(prefix="/sites", tags=["Sites"])

@router.post("/create")
def register_site(
    name: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(Site).filter(Site.name == name).first()
    if existing:
        raise HTTPException(400, "Site exists")
    site = create_site(db, name, location)
    return {"msg": "Site created", "site_id": site.id, "qr_code": site.qr_code}

@router.get("/all")
def get_all_sites(db: Session = Depends(get_db)):
    sites = db.query(Site).all()
    return [
        {
            "id": s.id,
            "site_name": s.name,
            "location": s.location
        } for s in sites
    ]

@router.get("/{site_id}/qr_image")
def get_qr_image(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(404, "Site not found")
    img = qrcode.make(site.qr_code)
    buf = BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@router.post("/assign-employee")
def assign_employee_to_site(
    site_id: int = Form(...),
    emp_code: str = Form(...),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(404, "Site not found")
    
    emp = db.query(Employee).filter(Employee.emp_code == emp_code).first()
    if not emp:
        raise HTTPException(404, "Employee not found")
    
    exists = db.query(SiteEmployeeAssignment).filter(
        SiteEmployeeAssignment.site_id == site_id,
        SiteEmployeeAssignment.employee_id == emp.id
    ).first()
    if exists:
        raise HTTPException(400, "Already assigned")
    
    assignment = SiteEmployeeAssignment(site_id=site_id, employee_id=emp.id)
    db.add(assignment)
    db.commit()
    return {"msg": f"{emp_code} assigned to {site.name}"}