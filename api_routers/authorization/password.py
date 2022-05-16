from passlib.context import CryptContext
from sqlalchemy.orm import Session

from schemas import UserModel
from store import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session: Session, username: str, password: str):
    user = get_user(session, UserModel(nickname=username))
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
