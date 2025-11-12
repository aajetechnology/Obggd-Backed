from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user import create_user, authenticate
from app.schemas.user import UserCreate
from pydantic import BaseModel
from app.models.user import User

# TOKEN MODEL (WAS MISSING)
class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email taken")
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(400, "Phone taken")
    
    new_user = create_user(db, user)
    return {
        "msg": "SUCCESS Worker Registered!",
        "employee_id": new_user.employee_id,
        "name": new_user.name,
        "department": new_user.department,
        "profile_pic": new_user.profile_pic,
            "login_now": {
                "email": new_user.email,
                "password": user.password
            }
    }

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(401, "Wrong email/password")
    return {
        "access_token": f"jwt-{user.employee_id}",
        "token_type": "bearer",
        "user": {
            "id": user.employee_id,
            "name": user.name,
            "phone": user.phone,
            "department": user.department,
            "pic": user.profile_pic
        }
    }