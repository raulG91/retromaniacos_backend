import os
from sqlmodel import SQLModel, create_engine, Session
from  fastapi import Depends
from typing import Annotated
from .models.user import User
from .models.event import Event

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Using database URL: {DATABASE_URL}")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True, future=True)

def create_db_and_tables():
   # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("Database and tables created")

#Function to be used as dependency to get DB session

def getSession():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(getSession)]