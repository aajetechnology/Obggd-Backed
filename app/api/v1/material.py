# app/api/v1/material.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.employee import Employee
from app.models.material import MaterialRequest  # ← THIS WAS MISSING!
from pydantic import BaseModel
from typing import Optional
from app.crud.material import (
    create_request, approve_request, decline_request, 
    confirm_delivery, get_requests_by_employee,
    get_pending_requests_crud  
)

router = APIRouter(prefix="/material", tags=["Material Requests"])

class MaterialRequestCreate(BaseModel):
    emp_code: str
    material: str
    quantity: str
    notes: Optional[str] = None

class DeclineRequest(BaseModel):
    reason: str

@router.post("/request")
def request_material(
    emp_code: str = Form(...),
    material: str = Form(...),
    quantity: str = Form(...),
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    req = create_request(
        db,
        emp_code, 
        material, 
        quantity, 
        notes
    )
    return {"msg": "Request sent", "request_id": req.id}

@router.get("/my-requests/{emp_code}")
def my_requests(emp_code: str, db: Session = Depends(get_db)):
    requests = get_requests_by_employee(db, emp_code)
    result = []
    for r in requests:
        employee = db.query(Employee).filter(Employee.emp_code == r.emp_code).first()
        result.append({
            "id": r.id,
            "material": r.material,
            "quantity": r.quantity,
            "notes": r.notes or "",
            "status": r.status,
            "requested_at": r.requested_at.isoformat() if r.requested_at else None,
            "emp_code": r.emp_code,
            "employee_name": employee.name if employee else "Unknown",
            "employee_role": employee.role if employee else "Worker"
        })
    return result

@router.get("/pending")
def get_pending_requests(db: Session = Depends(get_db)):
    # 1. Call the specific CRUD function from material.py
    requests = get_pending_requests_crud(db) 
    
    result = []
    for r in requests:
        # 2. Resolve the employee name for the Desktop UI
        employee = db.query(Employee).filter(Employee.emp_code == r.emp_code).first()
        
        result.append({
            "id": r.id,
            "material": r.material,
            "quantity": r.quantity,
            "notes": r.notes or "",
            "status": r.status,
            # 3. Format the date so the Desktop can slice it [:10]
            "requested_at": r.requested_at.isoformat() if r.requested_at else None,
            "employee_name": employee.name if employee else "Unknown Worker"
        })
    return result
    
@router.post("/approve/{req_id}")
def approve(req_id: int, db: Session = Depends(get_db)):
    req = approve_request(db, req_id, "MGR001")
    if not req:
        raise HTTPException(400, "Cannot approve")
    return {"msg": "Approved", "eta": req.eta}

@router.post("/decline/{req_id}")
def decline(req_id: int, payload: DeclineRequest, db: Session = Depends(get_db)):
    req = decline_request(db, req_id, "MGR001", payload.reason)
    if not req:
        raise HTTPException(400, "Cannot decline")
    return {"msg": "Declined", "reason": req.decline_reason}

@router.post("/deliver/{req_id}")
def deliver(req_id: int, db: Session = Depends(get_db)):
    req = confirm_delivery(db, req_id)
    if not req:
        raise HTTPException(400, "Invalid delivery")
    return {"msg": "Delivered"}