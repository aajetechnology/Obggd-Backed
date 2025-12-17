# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, Base
from app.api.v1.user import router as user_router
from app.api.v1 import auth_router, site_router, user_router, log_router, material_router, attendance_router, qrcode_router

app = FastAPI(title="OBGGD Construction Empire", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(site_router)
app.include_router(user_router)
app.include_router(log_router)
app.include_router(material_router)
app.include_router(attendance_router)
app.include_router(user_router)
app.include_router(qrcode_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"msg": "OBGGD Backend Running – Ready for Mobile & Desktop Apps!"}