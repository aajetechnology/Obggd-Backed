# create_tables.py — RUN THIS ONCE ONLY!
from app.core.database import Base, engine
from app.models.material import MaterialRequest  # ← make sure this line is here

print("Creating material_requests table...")

Base.metadata.create_all(bind=engine)

print("Table created successfully! GLORY TO OBGGD!")