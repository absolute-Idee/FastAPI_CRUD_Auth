from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from app.backend.schemas import TokenPayload, SystemUser

from .database import SessionLocal
from app.backend import models


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)



async def get_current_user(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=400, detail='Token expired', headers={"WWW-Authentificate": "Bearer"})

    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail='Couldn\'t validate credentials', headers={"WWW-Authentificate": "Bearer"})

    db = SessionLocal()
    user = db.query(models.User).filter(models.User.username == token_data.sub).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=404, detail='No such user registered')

    return user
    