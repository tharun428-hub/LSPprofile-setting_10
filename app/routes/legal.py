from fastapi import APIRouter

router = APIRouter(prefix="/legal", tags=["Legal"])


#terms & conditions 
@router.get("/terms")
def terms():
    return {
        "title": "Terms & Conditions",
        "content": "These are the terms and conditions of the application."
    }


#privacy policy  
@router.get("/privacy-policy")
def privacy_policy():
    return {
        "title": "Privacy Policy",
        "content": "This application respects user privacy and data protection."
    }


# app version 
@router.get("/app-version")
def app_version():
    return {
        "version": "1.0.0"
    }