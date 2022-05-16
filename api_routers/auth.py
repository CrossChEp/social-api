from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api_routers.authorization import get_current_user, login_for_token
from api_routers.authorization.schemas.models import Token
from schemas import UserModel
from store import get_session

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           session: Session = Depends(get_session)):
    return login_for_token(session=session, form_data=form_data)


@auth_router.get('/user/me', response_model=UserModel)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

