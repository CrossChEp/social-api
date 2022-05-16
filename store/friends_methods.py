from sqlalchemy.orm import Session

from schemas import UserModel
from store import Friend, User, get_user
from store.requests_handler import get_requests


def get_friend(uid: int, session: Session):
    all_friends = []
    friends = session.query(User).filter_by(id=uid).first().friends
    for friend in friends:
        friend: Friend
        all_friends.append(get_user(session, UserModel(id=friend.friend_id)))
    return all_friends


def add_friend(uid: int, friend_id: int, session: Session):
    friend1 = Friend(
        friend_id=uid
    )
    friend2 = Friend(
        friend_id=friend_id
    )

    session.add(friend1)
    session.add(friend2)
    user_1 = session.query(User).filter_by(id=uid).first()
    user_2 = session.query(User).filter_by(id=friend_id).first()
    user_1.friends.append(friend2)
    user_2.friends.append(friend1)
    session.commit()


def delete_friend(uid: int, friend_id: int, session: Session):
    user_1 = session.query(Friend).filter_by(user_id=uid, friend_id=friend_id).first()
    user_2 = session.query(Friend).filter_by(user_id=friend_id, friend_id=uid).first()
    session.delete(user_1)
    session.delete(user_2)
    session.commit()


def requests_get(uid: int, session: Session):
    user_requests = get_requests()
    friend_requests = []
    output_friends = {}
    for request in user_requests.values():
        if request['user_receiver'] == uid:
            user = get_user(session=session, user=UserModel(id=request['user_sender']))
            friend_requests.append(user.nickname)
    output_friends.update({'friend_requests': friend_requests})
    return output_friends


def sent_invites_get(uid, session: Session):
    requests = get_requests()
    sent_requests = []
    output_requests = {}
    for request in requests.values():
        if request['user_sender'] == uid:
            user = get_user(session=session, user=UserModel(id=request['user_receiver']))
            sent_requests.append(user.nickname)
    output_requests.update({'sent_requests': sent_requests})
    return output_requests
