from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_routers.authorization import get_current_user
from schemas import PostModel, UserModel
from store import User, get_session
from api_routers.users import get_user
from store.posts_methods import create_post, get_posts, get_all_posts_ever

posts_router = APIRouter()


@posts_router.get("/users/{uid}/posts")
def get_user_posts(uid: int, session: Session = Depends(get_session)):
    if get_user(session, UserModel(id=uid)):
        return get_posts(uid, session)
    else:
        raise HTTPException(status_code=404)


@posts_router.post("/users/posts")
def add_post(post: PostModel, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if post.content == "":
        raise HTTPException(status_code=400, detail="Content must be not None")

    create_post(post, user, session)


@posts_router.get('/posts')
def get_all_posts(session: Session = Depends(get_session)):
    return get_all_posts_ever(session)
