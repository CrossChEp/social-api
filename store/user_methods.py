from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query

from schemas import UserModel
from store import User
from store import sessionmaker


def get_user(session: Session, user: UserModel):
    if not user.__dict__:
        raise ValidationError("No user data given")
    params = {}
    for key, val in user.__dict__.items():
        if val is not None:
            params[key] = val

    return session.query(User).filter_by(**params).first()


def get_all_users(session: Session):
    rec: Query = session.query(User).select_from(User)
    data = rec.all()
    return data


def get_user_by_email(session: Session, email: str) -> User:
    user = None
    try:
        user = session.query(User).filter_by(email=email).one()
    except NoResultFound:
        raise NoResultFound("No user with such email")
    session.expunge_all()
    return user


