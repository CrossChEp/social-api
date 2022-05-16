from store import get_user
from store import session, User
from sqlalchemy.orm import Query


def is_user_exists(email: str, password: str = ''):
    """
    Function gets user's email and password.
    Returns user's json if user exists, else returns None
    """
    with session.begin() as sess:

        if password == '':
            query = sess.query(User).filter_by(email=email).scalar() is not None
        else:

            query = sess.query(User).filter_by(email=email, password=password).scalar() is not None

        if query:
            #  getting users from db, that have the same password and email
            req: Query = sess.query(User).select_from(User).where(User.email == email, User.password == password)
            user_id = req.all().id
            return get_user(user_id)

        else:
            return None
