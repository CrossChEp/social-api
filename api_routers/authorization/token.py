from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api_routers.authorization.password import authenticate_user
from api_routers.authorization.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from api_routers.authorization.schemas.models import Token
from store import User


def create_access_token(uid: int):
    to_encode = {"id": uid}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def login_for_token(session: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = authenticate_user(session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.id)
    return Token(access_token=token, token_type="bearer")
