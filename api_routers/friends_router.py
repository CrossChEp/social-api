from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import UserModel
from store import User, add_friend, delete_friend, get_friend, get_session, requests_get, sent_invites_get
from api_routers.authorization.authorization import get_current_user
from store.requests_handler import create_request, get_requests, parse_request
import store.requests_handler

friends_router = APIRouter()


@friends_router.post('/friend/invite')
def send_invite(rec_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return create_request(user.id, rec_id)


@friends_router.get('/friends/')
def get_friends(user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return get_friend(uid=user.id, session=session)


@friends_router.post('/friend/accept')
def accept_friend(req_id: int, current_user: UserModel = Depends(get_current_user),
                  session: Session = Depends(get_session)):
    request = parse_request(req_id)
    if request == {}:
        raise HTTPException(status_code=404)

    add_friend(request["user_sender"], request["user_receiver"], session)


@friends_router.delete('/friends/delete')
def friend_delete(friend_id: int,
                  current_user: UserModel = Depends(get_current_user),
                  session: Session = Depends(get_session)):
    return delete_friend(
        uid=current_user.id,
        friend_id=friend_id,
        session=session
    )


@friends_router.get('/friends/requests')
def get_friend_requests(user: UserModel = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    return requests_get(uid=user.id, session=session)


@friends_router.delete('/friends/request')
def delete_request(request_id: int, user: User = Depends(get_current_user)):
    try:
        store.requests_handler.delete_request(request_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@friends_router.get('/friends/sent/invites')
def get_sent_invites(user: UserModel = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    return sent_invites_get(uid=user.id, session=session)


@friends_router.get('/friends/all/requests')
def get_all_requests():
    return get_requests()
