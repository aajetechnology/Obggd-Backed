from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.attendance import assign_worker, clock_in, get_site_workers
from app.models.user import User
from app.models.site import Site
from datetime import date

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/assign")
def assign(emp_id: str, site_id: int, db: Session = Depends(get_db)):
    assign_worker(db, emp_id, site_id)
    return {"msg": f"{emp_id} assigned to site {site_id}"}

@router.post("/clock-in")
def clock_in_api(emp_id: str, site_id: int, db: Session = Depends(get_db)):
    record = clock_in(db, emp_id, site_id)
    return {
        "msg": "Clocked In!",
        "employee_id": emp_id,
        "time": record.clock_in.strftime("%H:%M"),
        "status": "present"
    }

@router.get("/site/{site_id}")
def site_dashboard(site_id: int, db: Session = Depends(get_db)):
    workers = get_site_workers(db, site_id)
    site = db.query(Site).filter(Site.id == site_id).first()
    head = None
    if site and site.head_id:
        head_user = db.query(User).filter(User.employee_id == site.head_id).first()
        head = head_user.name if head_user else "Not Set"
    
    return {
        "site": site.name if site else "Unknown Site",
        "site_head": head or "Not Assigned",
        "total_workers": len(workers),
        "present_today": len([w for w in workers if w["status"] == "present"]),
        "workers": [
            {
                "employee_id": w["employee_id"],
                "name": w["name"],
                "status": w["status"],
                "clock_in": w["clock_in"],
                "color": "red" if w["status"] == "absent" else "green"
            }
            for w in workers
        ]
    }