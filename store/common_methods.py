import os.path

from sqlalchemy.exc import ArgumentError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta as Meta


def add(session, obj: Meta):
    session: Session
    session.add(obj)
    session.commit()


def delete(session: Session, table: Meta, uid: int):
    try:
        user = session.query(table).filter_by(id=uid).one()
    except ArgumentError:
        raise ArgumentError("Not such table")
    except NoResultFound:
        raise NoResultFound("There is no object with given id")
    else:
        session.delete(user)
        session.commit()
