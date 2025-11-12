from sqlalchemy.orm import Session
from app.models.material import MaterialRequest

def create_request(db: Session, emp_id: str, material: str, quantity: str, notes: str):
    req = MaterialRequest(
        employee_id=emp_id,
        material=material,
        quantity=quantity,
        notes=notes
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def approve_request(db: Session, req_id: int, manager_id: str):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if req:
        req.status = "Approved"
        req.approved_by = manager_id
        db.commit()
    return req

def start_delivery(db: Session, req_id: int):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if req:
        req.status = "In Transit"
        db.commit()
    return req

def confirm_delivery(db: Session, req_id: int):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if req:
        req.status = "Delivered"
        req.delivered_at = datetime.utcnow()
        db.commit()
    return req