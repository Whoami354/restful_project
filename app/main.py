from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, generator, templates, media, posts, converter, lists, spotify
from starlette.middleware.sessions import SessionMiddleware
from database import get_database
from auth import router as auth

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    SessionMiddleware,
    secret_key="YOUR_SECRET_KEY",
    max_age=1800,  # 30 minutes
    session_cookie="session"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(users.router)
app.include_router(generator.router)
app.include_router(templates.router)
#app.include_router(lists.router)
app.include_router(media.router)
app.include_router(posts.router)
app.include_router(converter.router)
app.include_router(lists.router)
app.include_router(spotify.router)
