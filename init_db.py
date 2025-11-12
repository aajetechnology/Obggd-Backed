from app.core.database import Base, engine
from app.models import user, qrcode  # BOTH

print("Building EMPIRE DB...")
Base.metadata.create_all(bind=engine)
print("Done! Tables: users (with ID), qrcodes")