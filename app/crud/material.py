from sqlalchemy.orm import Session
from app.models.material import MaterialRequest
from datetime import datetime
from sqlalchemy import func

def create_request(db: Session, emp_code: str, material: str, quantity: str, notes: str = ""):
    req = MaterialRequest(
        emp_code=emp_code,
        material=material,
        quantity=quantity,
        notes=notes or None,
        status="pending"
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def approve_request(db: Session, req_id: int, manager_id: str):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req or req.status != "pending":
        return None
    req.status = "approved"
    req.approved_by = manager_id
    req.approved_at = func.now()
    req.eta = 45
    db.commit()
    db.refresh(req)
    return req

def decline_request(db: Session, req_id: int, manager_id: str, reason: str):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req or req.status != "pending":
        return None
    req.status = "declined"
    req.declined_by = manager_id
    req.declined_at = func.now()
    req.decline_reason = reason.strip() or "No reason provided"
    db.commit()
    db.refresh(req)
    return req

def confirm_delivery(db: Session, req_id: int):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req or req.status not in ["in_transit", "approved"]:
        return None
    req.status = "delivered"
    req.delivered_at = datetime.utcnow()
    db.commit()
    db.refresh(req)
    return req

def get_requests_by_employee(db: Session, emp_code: str):
    return db.query(MaterialRequest).filter(MaterialRequest.emp_code == emp_code).order_by(MaterialRequest.requested_at.desc()).all()

def get_pending_requests_crud(db: Session):
    """Fetches all requests that need manager approval."""
    return db.query(MaterialRequest).filter(MaterialRequest.status == "pending").order_by(MaterialRequest.requested_at.desc()).all()