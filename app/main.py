from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.api.v1 import qr_router, auth_router, material_router, attendance_router, log_router, user_router



app = FastAPI(title="OBGGD EMPIRE")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(qr_router)
app.include_router(material_router)
app.include_router(attendance_router)
app.include_router(log_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"msg": "OBGGD EMPIRE — LOGIN + QR = UNSTOPPABLE"}