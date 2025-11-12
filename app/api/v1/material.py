from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.material import create_request, approve_request, start_delivery, confirm_delivery

router = APIRouter(prefix="/material", tags=["Material Request"])

@router.post("/request")
def request(emp_id: str, material: str, quantity: str, notes: str = "", db: Session = Depends(get_db)):
    req = create_request(db, emp_id, material, quantity, notes)
    return {
        "msg": "Request Sent!",
        "request_id": req.id,
        "status": req.status,
        "eta": req.eta
    }

@router.post("/approve/{req_id}")
def approve(req_id: int, manager_id: str, db: Session = Depends(get_db)):
    req = approve_request(db, req_id, manager_id)
    return {"msg": "Approved! Truck dispatched", "map_url": f"/track/{req_id}"}

@router.get("/track/{req_id}")
def track(req_id: int, db: Session = Depends(get_db)):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == req_id).first()
    if not req: return {"error": "Not found"}
    return {
        "request_id": req_id,
        "material": req.material,
        "status": req.status,
        "eta": req.eta,
        "live_map": f"https://obggd.com/map?track={req_id}",
        "driver_phone": "080-1234-5678"
    }

@router.post("/deliver/{req_id}")
def deliver(req_id: int, db: Session = Depends(get_db)):
    req = confirm_delivery(db, req_id)
    return {"msg": "Delivered & Confirmed!", "status": "Delivered"}