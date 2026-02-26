from fastapi import APIRouter

router = APIRouter(prefix="/legal", tags=["Legal"])



@router.get("/terms")
def terms():
    return {
        "title": "Terms & Conditions",
        "content": "These are the terms and conditions of the application."
    }



@router.get("/privacy-policy")
def privacy_policy():
    return {
        "title": "Privacy Policy",
        "content": "This application respects user privacy and data protection."
    }



@router.get("/app-version")
def app_version():
    return {
        "version": "1.0.0"
    }