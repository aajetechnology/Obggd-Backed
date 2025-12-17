from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.employee import Employee
from app.models.site import Site
from app.models.attendance import DailyAttendance
from app.models.site_assignment import SiteEmployeeAssignment
from app.crud.attendance import assign_worker, clock_in, get_site_workers
from app.core.security import get_current_employee
from datetime import datetime, date
from pydantic import BaseModel

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# Pydantic model for JSON requests from React Native
class ScanRequest(BaseModel):
    qr_code: str
    emp_id: str

@router.post("/scan")
async def scan_attendance(data: ScanRequest, db: Session = Depends(get_db)):
    """
    Handles both Clock-In and Clock-Out via a single QR Scan.
    Works with JSON data from React Native 'api.post'
    """
    # 1. Parse Site ID from QR Code String
    # Format expected: "OBGGD:SITE:Name|LOC:City|ID:1"
    try:
        if "ID:" not in data.qr_code:
            raise ValueError("Invalid QR Format")
        site_id_str = data.qr_code.split("ID:")[-1]
        site_id = int(site_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Site QR Code Format")

    # 2. Verify Site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found in database")

    # 3. Verify Employee exists
    employee = db.query(Employee).filter(Employee.emp_code == data.emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # 4. Verify Assignment (Is this worker allowed to be at this site?)
    assignment = db.query(SiteEmployeeAssignment).filter(
        SiteEmployeeAssignment.employee_id == employee.id,
        SiteEmployeeAssignment.site_id == site.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=403, detail="You are not assigned to this site!")

    # 5. Handle Attendance Logic (Check-in vs Check-out)
    today = date.today()
    record = db.query(DailyAttendance).filter(
        DailyAttendance.employee_id == data.emp_id,
        DailyAttendance.site_id == site.id,
        DailyAttendance.date == today
    ).first()

    now = datetime.utcnow()

    if not record:
        # Action: Check-In
        record = DailyAttendance(
            employee_id=data.emp_id,
            site_id=site.id,
            date=today,
            clock_in=now,
            status="present"
        )
        db.add(record)
        db.commit()
        return {
            "success": True,
            "action": "check_in",
            "msg": f"Welcome to {site.name}!",
            "time": now.strftime("%H:%M")
        }

    elif record.clock_in and not record.clock_out:
        # Action: Check-Out
        record.clock_out = now
        db.commit()
        return {
            "success": True,
            "action": "check_out",
            "msg": "Safe journey home! Clock-out recorded.",
            "time": now.strftime("%H:%M")
        }

    else:
        # Already finished for today
        raise HTTPException(status_code=400, detail="You have already clocked out for today.")

# Other Helper Routes
@router.get("/assignments/{site_id}")
def get_assignments(site_id: int, db: Session = Depends(get_db)):
    return get_site_workers(db, site_id)

@router.post("/assign")
def assign_worker_to_site(emp_code: str = Form(...), site_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        assign_worker(db, emp_code, site_id)
        return {"msg": "Assigned successfully"}
    except ValueError as e:
        raise HTTPException(404, str(e))