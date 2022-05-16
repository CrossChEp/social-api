from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store.db_model import User, Post, Message, Friend
from store.common_methods import add, delete
from store.messages_methods import get_messages, update_message, delete_message, add_message, get_messages_greater, get_messages_less, get_messages_last
from store.user_methods import get_user, get_user_by_email, get_all_users
from store.friends_methods import add_friend, get_friend, delete_friend, requests_get, sent_invites_get
from store.image_methods import decode_image, encode_image

database_protocol = "sqlite:///store/database.db"
engine = create_engine(database_protocol, echo=True, connect_args={"check_same_thread": False})
session = sessionmaker(bind=engine)


def get_session():
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
