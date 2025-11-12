from sqlalchemy.orm import Session
from app.models.attendance import WorkerSiteAssignment, DailyAttendance
from app.models.site import Site
from datetime import date

def assign_worker(db: Session, emp_id: str, site_id: int):
    assignment = WorkerSiteAssignment(employee_id=emp_id, site_id=site_id)
    db.add(assignment)
    db.commit()
    return assignment

def clock_in(db: Session, emp_id: str, site_id: int):
    today = date.today()
    record = db.query(DailyAttendance).filter(
        DailyAttendance.employee_id == emp_id,
        DailyAttendance.site_id == site_id,
        DailyAttendance.date == today
    ).first()
    if not record:
        record = DailyAttendance(employee_id=emp_id, site_id=site_id, date=today)
        db.add(record)
    record.clock_in = datetime.utcnow()
    record.status = "present"
    db.commit()
    return record

def get_site_workers(db: Session, site_id: int, today=date.today()):
    assignments = db.query(WorkerSiteAssignment).filter(WorkerSiteAssignment.site_id == site_id).all()
    workers = []
    for a in assignments:
        attendance = db.query(DailyAttendance).filter(
            DailyAttendance.employee_id == a.employee_id,
            DailyAttendance.date == today
        ).first()
        workers.append({
            "employee_id": a.employee_id,
            "name": db.query(User).filter(User.employee_id == a.employee_id).first().name,
            "status": attendance.status if attendance else "absent",
            "clock_in": attendance.clock_in.strftime("%H:%M") if attendance and attendance.clock_in else None
        })
    return workers