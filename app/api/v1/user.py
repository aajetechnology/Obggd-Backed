from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User  # ← Your model
from app.schemas.user import UserOut  # ← Your schema (optional)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/workers")
def get_workers(db: Session = Depends(get_db)):
    workers = db.query(User).filter(User.role == "worker").all()
    return[UserOut.from_orm(w) for w in workers]