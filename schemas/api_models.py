from typing import List, Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id: Optional[int]
    nickname: Optional[str]
    password: Optional[str]
    email: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class GetUserModel(BaseModel):
    nickname: str
    password: str
    email: str
    avatar: Optional[str]

    class Config:
        orm_mode = True


class UpdateUserModel(BaseModel):
    nickname: Optional[str]
    password: Optional[str]
    email: Optional[str]
    avatar: Optional[str]


class MessageModel(BaseModel):
    content: str
    sender_id: int
    receiver_id: int

    class Config:
        orm_mode = True


class MessageGet(MessageModel):
    id: int

    class Config:
        orm_mode = True


class PostModel(BaseModel):
    content: str


class Dialog(BaseModel):
    sender: List[MessageGet]
    receiver: List[MessageGet]

    class Config:
        orm_mode = True
