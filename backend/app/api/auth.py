from fastapi import APIRouter

router = APIRouter(prefix="/api/auth")

@router.get("/status")
def status():
    return {
        "auth": "ready",
        "methods": [
            "password",
            "email_code",
            "wechat",
            "sms_switch"
        ]
    }
