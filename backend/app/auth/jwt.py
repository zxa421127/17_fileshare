from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "CHANGE_ME_IN_PRODUCTION"
ALGORITHM = "HS256"

def create_token(user_id:int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow()+timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
