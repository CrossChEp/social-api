from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from api_routers.authorization.config import ALGORITHM, SECRET_KEY
from api_routers.authorization.schemas.models import TokenData
from schemas import UserModel
from store import get_session, get_user
#from store import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        uid: int = int(payload.get("id"))
        if uid is None:
            raise credentials_exception
        token_data = TokenData(id=uid)
    except JWTError:
        raise credentials_exception

    exp = payload.get("exp")
    if exp is None:
        raise credentials_exception
    exp = datetime.utcfromtimestamp(exp)
    if exp < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    user = get_user(session, UserModel(id=token_data.id))
    if user is None:
        raise credentials_exception
    return user
