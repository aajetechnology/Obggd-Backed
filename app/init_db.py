from app.core.database import Base, engine
from app.models import qrcode

print("Building fresh DB...")
Base.metadata.create_all(bind=engine)
print("Done! Table: qrcodes")