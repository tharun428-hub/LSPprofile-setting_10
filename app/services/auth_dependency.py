from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.auth import oauth2_scheme, SECRET_KEY, ALGORITHM


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )