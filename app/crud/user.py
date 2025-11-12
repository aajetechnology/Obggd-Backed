from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import hashlib

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

def create_user(db: Session, user: UserCreate):
    last = db.query(User).order_by(User.id.desc()).first()
    emp_id = f"OBGGD-{1000 + (last.id if last else 0) + 1}EMP"
    
    hashed = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed,
        role=user.role,
        employee_id=emp_id,
        profile_pic=user.profile_pic or f"/pics/{emp_id}.jpg"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and user.password == hash_password(password):
        return user
    return None