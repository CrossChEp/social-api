from sqlalchemy import Column, INTEGER, VARCHAR, ForeignKey, String, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    nickname = Column(VARCHAR)
    email = Column(VARCHAR, nullable=True)
    password = Column(VARCHAR)
    avatar = Column(String)
    messages = relationship("Message", backref="user")
    posts = relationship("Post", backref="user")
    friends = relationship('Friend', backref='user')


class Message(base):
    __tablename__ = "messages"
    id = Column(INTEGER, primary_key=True)
    content = Column(String)
    sender_id = Column(INTEGER, ForeignKey("users.id"))
    receiver_id = Column(INTEGER)
    date = Column(String)


class Post(base):
    __tablename__ = "posts"
    id = Column(INTEGER, primary_key=True)
    author_id = Column(INTEGER, ForeignKey("users.id"))
    content = Column(String)


class Friend(base):
    __tablename__ = "friends"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    friend_id = Column(INTEGER)
