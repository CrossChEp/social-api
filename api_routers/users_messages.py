from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api_routers.authorization import get_current_user
from store import get_session, User
from store import add_message, delete_message, get_messages, update_message, get_messages_greater, get_messages_less, get_messages_last

msg_router = APIRouter()


@msg_router.get('/messages')
def get_msg(receiver_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_messages(sender_id=user.id, receiver_id=receiver_id, session=session)


@msg_router.post('/messages')
def send_message(receiver_id: int, content: str,
                 user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    try:
        return add_message(receiver_id=receiver_id, sender_id=user.id, content=content, session=session)
    except AttributeError:
        raise HTTPException(404, 'user not found')


@msg_router.delete('/messages/delete')
def delete_msg(message_id: int, session: Session = Depends(get_session)):
    try:
        return delete_message(message_id=message_id, session=session)
    except AttributeError:
        raise HTTPException(404, 'user not found')


@msg_router.put('/messages/{message_id}/update')
def update_msg(message_id: int, content: str, session: Session = Depends(get_session)):
    try:
        return update_message(message_id=message_id, content=content, session=session)
    except AttributeError:
        raise HTTPException(404, 'user not found')


@msg_router.get('/messages/upd')
def get_msg_greater(receiver_id: int, id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_messages_greater(sender_id=user.id, receiver_id=receiver_id, id=id, session=session)


@msg_router.get('/messages/prev/')
def get_msg_less(receiver_id: int, id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_messages_less(sender_id=user.id, receiver_id=receiver_id, id=id, session=session)

@msg_router.get('/messages/last/')
def get_msg_last(receiver_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_messages_last(sender_id=user.id, receiver_id=receiver_id, session=session)
