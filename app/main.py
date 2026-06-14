from fastapi import FastAPI
from .db.database import engine, Base
from .routers import auth, ventures, chat, history
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ventures.router)
app.include_router(chat.router)
app.include_router(history.router)