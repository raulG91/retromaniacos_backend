from fastapi import FastAPI
from .routes.user import userRouter
from .routes.event import eventRouter
from .db import create_db_and_tables
import os

app = FastAPI()
#On startup event, create the database and tables if needed
@app.on_event("startup")
def on_startup():
    if os.getenv("APP_ENV") != "test" :
        print("Creating database and tables...")
        create_db_and_tables()



app.include_router(userRouter)
app.include_router(eventRouter)