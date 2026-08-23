from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from .routes.user import userRouter
from .routes.event import eventRouter
from .routes.material import materialRouter
from .routes.event_participation import participationRouter
from .routes.event_material import eventMaterialRouter
from .db import create_db_and_tables
import os



print("Secret key",os.getenv("SECRET_KEY"))
app = FastAPI()
#On startup event, create the database and tables if needed
@app.on_event("startup")
def on_startup():
    if os.getenv("APP_ENV") != "test" :
        print("Creating database and tables...")
        create_db_and_tables()



app.include_router(userRouter)
app.include_router(eventRouter)
app.include_router(materialRouter)
app.include_router(participationRouter)
app.include_router(eventMaterialRouter)