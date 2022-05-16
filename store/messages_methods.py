import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from schemas import Dialog
from store import Message, User


def get_messages(session: Session, sender_id: int, receiver_id: int):
    sender = session.query(Message).filter_by(sender_id=sender_id, receiver_id=receiver_id).all()
    receiver = session.query(Message).filter_by(sender_id=receiver_id, receiver_id=sender_id).all()
    dialog = Dialog(sender=sender, receiver=receiver)
    messages = {
        'sender': dialog.sender,
        'receiver': dialog.receiver
    }
    return messages


def get_messages_greater(session: Session, id: int, sender_id: int, receiver_id: int):
    sender = session.query(Message).filter_by(sender_id=sender_id, receiver_id=receiver_id).filter(Message.id > id).limit(5).all()
    receiver = session.query(Message).filter_by(sender_id=receiver_id, receiver_id=sender_id).filter(Message.id > id).limit(5).all()
    merged = sender + receiver
    print(sender)
    print(merged)
    merged = sorted(merged, key=lambda x: x.id)
    merged = merged[:5]
    sender = []
    receiver = []
    for i in merged:
        if i.sender_id == sender_id:
            sender.append(i)
        else:
            receiver.append(i)
    dialog = Dialog(sender=sender, receiver=receiver)
    messages = {
        'sender': dialog.sender,
        'receiver': dialog.receiver
    }
    return messages


def get_messages_last(session: Session, sender_id: int, receiver_id: int):
    sender = session.query(Message).filter_by(sender_id=sender_id, receiver_id=receiver_id).order_by(-Message.id).limit(5).all()
    receiver = session.query(Message).filter_by(sender_id=receiver_id, receiver_id=sender_id).order_by(-Message.id).limit(5).all()
    merged = sender + receiver
    merged = sorted(merged, key=lambda x: x.id)
    merged = merged[:5]
    sender = []
    receiver = []
    for i in merged:
        if i.sender_id == sender_id:
            sender.append(i)
        else:
            receiver.append(i)
    dialog = Dialog(sender=sender, receiver=receiver)
    messages = {
        'sender': dialog.sender,
        'receiver': dialog.receiver
    }
    return messages
def get_messages_less(session: Session, id: int, sender_id: int, receiver_id: int):
    sender = session.query(Message).filter_by(sender_id=sender_id, receiver_id=receiver_id).filter(Message.id < id).order_by(-Message.id).limit(5).all()
    receiver = session.query(Message).filter_by(sender_id=receiver_id, receiver_id=sender_id).filter(Message.id < id).order_by(-Message.id).limit(5).all()
    merged = sender + receiver
    print(sender)
    print(merged)
    merged = sorted(merged, key=lambda x: -x.id)
    merged = merged[:5]
    sender = []
    receiver = []
    for i in merged:
        if i.sender_id == sender_id:
            sender.append(i)
        else:
            receiver.append(i)
    dialog = Dialog(sender=sender, receiver=receiver)
    messages = {
        'sender': dialog.sender,
        'receiver': dialog.receiver
    }
    return messages

def add_message(session: Session, receiver_id: int, sender_id: int, content: str):
    try:
        current_date = str(datetime.datetime.now())
        res = Message(
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id,
            date=current_date
        )
        user = session.query(User).filter_by(id=sender_id).one()
        session.add(res)
        user.messages.append(res)
        session.commit()
    except NoResultFound:
        raise AttributeError("No row was found when one was required")


def delete_message(session: Session, message_id: int):
    try:
        res = session.query(Message).filter_by(id=message_id).first()
        session.delete(res)
        session.commit()
    except UnmappedInstanceError:
        raise AttributeError("Class 'builtins.NoneType' is not mapped")


def update_message(session: Session, message_id: int, content: str):
    update_this = session.query(Message).filter_by(id=message_id).first()
    update_this.content = content
    session.commit()
