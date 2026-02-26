from fastapi import FastAPI
from app.core.database import Base, engine, SessionLocal
from app.core.default_data import create_default_users

# routers
from app.routes import auth, admin
from app.routes.profile_read import router as read_router
from app.routes.profile_address import router as address_router
from app.routes.language import router as language_router
from app.routes.notification import router as notification_router
from app.routes.email_otp import router as email_otp_router
from app.routes.user_privacy import router as privacy_router
from app.routes.admin_dashboard import router as admin_dashboard_router
from app.routes.admin_change_request import router as admin_change_router
from app.routes.legal import router as legal_router
from app.routes import user_settings
# models
import app.models.user
import app.models.user_profile
import app.models.user_settings
import app.models.consent


app = FastAPI(title="User Profile API")


# ===== STARTUP EVENT =====
@app.on_event("startup")
def startup_event():

    # create tables
    Base.metadata.create_all(bind=engine)

    # create default users
    db = SessionLocal()
    create_default_users()
    db.close()


# ===== PROFILE =====
app.include_router(read_router)
app.include_router(address_router)

# ===== EMAIL =====
app.include_router(email_otp_router)

# ===== LANGUAGE & NOTIFICATION =====
app.include_router(language_router)
app.include_router(notification_router)
app.include_router(user_settings.router)

# ===== PRIVACY =====
app.include_router(privacy_router)

# ===== LEGAL =====
app.include_router(legal_router)

# ===== AUTH =====
app.include_router(auth.router)

# ===== ADMIN =====
app.include_router(admin.router)

# ===== ADMIN MANAGEMENT =====
app.include_router(admin_change_router)
app.include_router(admin_dashboard_router)