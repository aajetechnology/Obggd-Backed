from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str = "worker"
    department: str = "General"   # YOU TYPE THIS
    profile_pic: Optional[str] = None


class UserOut(BaseModel):
    employee_id: str
    name: str
    role: str

    class Config:
        from_attributes = True