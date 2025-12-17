from sqlalchemy.orm import Session
from app.models.attendance import DailyAttendance
from app.models.site_assignment import SiteEmployeeAssignment
from app.models.employee import Employee
from datetime import date, datetime

def assign_worker(db: Session, emp_code: str, site_id: int):
    employee = db.query(Employee).filter(Employee.emp_code == emp_code).first()
    if not employee:
        raise ValueError("Employee not found")
    # Remove old assignments (one site per worker)
    db.query(SiteEmployeeAssignment).filter(SiteEmployeeAssignment.employee_id == employee.id).delete()
    assignment = SiteEmployeeAssignment(employee_id=employee.id, site_id=site_id)
    db.add(assignment)
    db.commit()
    return assignment

def clock_in(db: Session, emp_code: str, site_id: int):
    today = date.today()
    record = db.query(DailyAttendance).filter(
        DailyAttendance.employee_id == emp_code,
        DailyAttendance.site_id == site_id,
        DailyAttendance.date == today
    ).first()
    if not record:
        record = DailyAttendance(employee_id=emp_code, site_id=site_id, date=today)
        db.add(record)
    record.clock_in = datetime.utcnow()
    record.status = "present"
    db.commit()
    return record

def get_site_workers(db: Session, site_id: int, today=date.today()):
    assignments = db.query(SiteEmployeeAssignment).filter(SiteEmployeeAssignment.site_id == site_id).all()
    workers = []
    for a in assignments:
        attendance = db.query(DailyAttendance).filter(
            DailyAttendance.employee_id == a.employee.emp_code,
            DailyAttendance.date == today
        ).first()
        workers.append({
            "employee_id": a.employee.emp_code,
            "name": a.employee.name,
            "status": attendance.status if attendance else "absent",
            "clock_in": attendance.clock_in.strftime("%H:%M") if attendance and attendance.clock_in else None
        })
    return workers