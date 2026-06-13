from fastapi import FastAPI
from .db.database import engine, Base
from .routers import auth,ventures, chat

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(ventures.router)
app.include_router(chat.router)