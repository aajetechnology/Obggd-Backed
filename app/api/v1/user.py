from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.employee import Employee
from app.core.security import get_current_employee
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None



@router.put("/update")
def update_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee)
):
    if payload.name is not None:
        current_employee.name = payload.name.strip()
    if payload.phone is not None:
        current_employee.phone = payload.phone.strip()
    if payload.email is not None:
        current_employee.email = payload.email.strip() or None

    db.commit()
    db.refresh(current_employee)

    return {"msg": "Profile updated successfully!"}
    
@router.get("/workers")
def get_workers(db: Session = Depends(get_db)):
    workers = db.query(Employee).filter(Employee.role == "worker").all()
    return [{"name": w.name, "emp_code": w.emp_code, "department": w.department, "phone": w.phone} for w in workers]

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return [{"emp_code": e.emp_code, "name": e.name, "role": e.role} for e in db.query(Employee).all()]