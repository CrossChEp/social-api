import base64
from typing import List

from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from fastapi import APIRouter, Depends, HTTPException
import bcrypt

from api_routers.authorization import get_current_user
from store import User, get_session, decode_image
from store import add, delete, get_all_users, get_user
from schemas import GetUserModel, UpdateUserModel, UserModel
from store.config import IMAGES

users_router = APIRouter()


@users_router.get("/users/{uid}", status_code=200, responses={404: {}}, response_model=UserModel)
def get_one_user(uid: int, session: Session = Depends(get_session)):
    user = get_user(session, UserModel(id=uid))
    if not user:
        raise HTTPException(status_code=404)
    return user


@users_router.get('/users/get/{nickname}', status_code=200, responses={404: {}}, response_model=UserModel)
def get_user_by_nickname(nickname: str, session: Session = Depends(get_session)):
    user = get_user(session, UserModel(nickname=nickname))
    if not user:
        raise HTTPException(status_code=404)
    return user


@users_router.get("/users/", response_model=List[UserModel])
def get_users(session: Session = Depends(get_session)) -> List[UserModel]:
    users = get_all_users(session)
    users = list(map(lambda x: UserModel.from_orm(x), users))
    return users


@users_router.post("/users/", status_code=200)
def add_new_user(user: GetUserModel, session: Session = Depends(get_session)):
    if user.nickname.lower() == 'con':
        raise HTTPException(status_code=406, detail='user with nickname "con" are not allowed')
    user.password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    )  # password hashing
    if user.avatar is None:
        with open(f"{IMAGES}/user_image.jpg", 'rb') as img:
            user.avatar = base64.encodebytes(img.read()).hex()

        with open(f'static/{user.nickname}.jpeg', 'wb') as pfp:
            image = decode_image(user.avatar)
            pfp.write(image)

    new_user = User(**user.dict())
    add(session, new_user)  # adding to database


@users_router.delete("/users/{uid}", status_code=200, responses={404: {}})
def user_deletion(uid: int, session: Session = Depends(get_session)):
    try:
        delete(session, User, uid)
    except NoResultFound:
        raise HTTPException(status_code=404)


@users_router.put("/users/update", status_code=200,
                  responses={404: {}, 400: {"description": "Data to change",
                                            "content": {
                                                "application/json": {
                                                    "example": {"username": "string", "password": "string",
                                                                "email": "string"}
                                                }}}})
def change_user(user: UpdateUserModel, current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):

    try:
        if user.nickname.lower() == 'con':
            raise HTTPException(status_code=406, detail='user with nickname "con" are not allowed')
    except AttributeError:
        pass
    data: dict = user.dict()
    data = dict(filter(lambda x: x[1] is not None, data.items()))
    req: Query = session.query(User).filter_by(id=current_user.id)
    if req.scalar() is None:
        raise HTTPException(status_code=404)
    if not data:
        raise HTTPException(status_code=400, detail="No data was given")

    if data.get("password") is not None:
        data["password"] = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
    req.update(data)
    if user.avatar is not None:
        with open(f'static/{req.first().nickname}.jpeg', 'wb') as img:
            pfp = decode_image(user.avatar)
            img.write(pfp)
        # if user.nickname is not None:
        #     with open(f'static/{user.nickname}.jpeg', 'wb') as img:
        #         pfp = decode_image(user.avatar)
        #         img.write(pfp)
        #
        # else:
        #     with open(f'static/{current_user.nickname}.jpeg', 'wb') as img:
        #         pfp = decode_image(user.avatar)
        #         img.write(pfp)
        # data['avatar'] = user.avatar
    session.commit()