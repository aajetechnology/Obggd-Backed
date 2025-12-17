# app/api/v1/__init__.py
from .auth import router as auth_router
from .site import router as site_router
from .user import router as user_router
from .log import router as log_router
from .material import router as material_router
from .attendance import router as attendance_router
from .qrcode import router as qrcode_router

__all__ = [
    "auth_router", "site_router", "user_router",
    "log_router", "material_router", "attendance_router", "qrcode_router"
]