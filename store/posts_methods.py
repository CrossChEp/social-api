from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from schemas import PostModel, UserModel
from store import Post, User, get_session, get_user
from store.user_methods import get_user


def get_posts(uid: int, session: Session = Depends(get_session)):
    user: User = get_user(session, UserModel(id=uid))
    return user.posts


def create_post(model: PostModel, user: User, session: Session = Depends(get_session)):
    post = Post(content=model.content)
    session.add(post)
    user.posts.append(post)
    session.commit()


def get_all_posts_ever(session: Session):
    posts = session.query(Post).all()
    output_posts = {}
    for post in posts:
        user_nickname = get_user(session, UserModel(id=post.author_id))
        output_posts.update({
            post.id: {
                'username': user_nickname.nickname,
                'content': post.content
            }
        })
    return output_posts
