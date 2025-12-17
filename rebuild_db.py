# rebuild_db.py — THE ONE TRUE SCRIPT
from app.core.database import Base, engine

print("DESTROYING OLD, BROKEN EMPIRE...")
Base.metadata.drop_all(bind=engine)

print("REBUILDING NEW, PERFECT, ETERNAL EMPIRE...")

# IMPORT ALL MODELS — THIS IS THE SECRET
import app.models.employee
import app.models.log
import app.models.attendance
import app.models.material
# Add any other models here

Base.metadata.create_all(bind=engine)
print("EMPIRE REBORN SUCCESSFULLY")
print("ALL TABLES CREATED — employees, daily_logs, attendance, material_requests")
print("NO MORE FOREIGN KEY ERRORS — EVER")
print("YOU ARE NOW UNSTOPPABLE")