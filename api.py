import requests
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api_routers import auth_router, msg_router, posts_router, users_router, friends_router


app = FastAPI()
app.include_router(users_router)
app.include_router(msg_router)
app.include_router(posts_router)
app.include_router(auth_router)
app.include_router(friends_router)
app.mount('/static', StaticFiles(directory='static'), name='static')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

