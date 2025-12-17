from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.core.database import get_db
from app.models.employee import Employee
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.security import decode_token
from sqlalchemy.orm import Session
from app.models.site_assignment import SiteEmployeeAssignment
import os



router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_employee(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    emp_code: str = payload.get("sub")
    if emp_code is None:
        raise credentials_exception
    employee = db.query(Employee).filter(Employee.emp_code == emp_code).first()
    if employee is None:
        raise credentials_exception
    return employee

# app/api/v1/auth.py — FINAL LOGIN (EMAIL + PHONE + emp_code)
@router.post("/login")
def login_with_email_or_phone(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    identifier = form_data.username.strip()
    password = form_data.password

    # Try all three: email → phone → emp_code
    employee = (
        db.query(Employee)
        .filter(
            (Employee.email == identifier) |
            (Employee.phone == identifier) |
            (Employee.emp_code == identifier)
        )
        .first()
    )

    if not employee or not verify_password(password, employee.password_hash):
        raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token = create_access_token(data={"sub": employee.emp_code})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "emp_code": employee.emp_code,
        "name": employee.name,
        "role": employee.role,
        "profile_pic": employee.profile_pic,
        "msg": "Welcome back!"
    }


from fastapi import Request

@router.post("/register")
async def register_employee(
    name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    email: str = Form(""),
    department: str = Form("General"),
    role: str = Form("worker"),
    profile_pic: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Check duplicates
    if db.query(Employee).filter(Employee.phone == phone).first():
        raise HTTPException(400, "Phone already registered")
    if email and db.query(Employee).filter(Employee.email == email).first():
        raise HTTPException(400, "Email already registered")

    # Generate emp_code
    last = db.query(Employee).order_by(Employee.id.desc()).first()
    num = (last.id + 1) if last else 1
    emp_code = f"OBGGD-{str(num).zfill(3)}"

    # Save profile pic — FULLY INDENTED
    profile_path = None
    if profile_pic and profile_pic.filename:
        ext = profile_pic.filename.split(".")[-1].lower()
        filename = f"{phone}.{ext}"
        save_path = f"static/profiles/{filename}"
        os.makedirs("static/profiles", exist_ok=True)
        content = await profile_pic.read()
        with open(save_path, "wb") as f:
            f.write(content)
        profile_path = f"/static/profiles/{filename}"

    # Hash password & save
    hashed = get_password_hash(password)
    employee = Employee(
        emp_code=emp_code,
        name=name,
        phone=phone,
        email=email or None,
        department=department,
        role=role,
        password_hash=hashed,
        profile_pic=profile_path
    )
    db.add(employee)
    db.commit()

    return {"msg": "Registered!", "emp_code": emp_code}

@router.get("/me")
async def read_current_employee(current_employee: Employee = Depends(get_current_employee), db:Session = Depends(get_db)):
    assignment = db.query(SiteEmployeeAssignment).filter(
        SiteEmployeeAssignment.employee_id == current_employee.id
    ).first()

    current_site = None
    if assignment:  
        site = db.query(Site).filter(Site.id == assignment.site_id).first()
        current_site = {"id": site.id, "name": site.name} if site else None
    return {
        "id": current_employee.emp_code,
        "name": current_employee.name,
        "role": current_employee.role,
        "pic": current_employee.profile_pic or "",
        "department": current_employee.department or "General",
        "email": current_employee.email or "Not set",
        "phone": current_employee.phone,
        "current_site_id": current_site.id if current_site else None,
        "current_site_name": current_site.name if current_site else "Not assigned"
        
    }