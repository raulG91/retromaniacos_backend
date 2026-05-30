import pytest
import os
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient
from app.main import app
from app.db import getSession  # Import the original dependency
from .test_util import create_random_email

# 1. Define your test database URL
TEST_DATABASE_URL = "mysql+pymysql://root:root@localhost/retromaniacos_test"
os.environ['APP_ENV'] = 'test'  # Set environment variable to indicate test mode
# 2. Create a separate engine for testing
test_engine = create_engine(TEST_DATABASE_URL, echo=True)
# 3. Create the override function
def get_session_override():
    """Override the getSession dependency to use the test database."""
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables in the test database before running any tests."""
    # Create all tables in the test database
    SQLModel.metadata.create_all(test_engine)
    yield
    # Optional: Drop all tables after tests are done
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(scope="session")
def client():
    """Provide a test client with the overridden dependency."""
    # Override the getSession dependency to use the test session
    app.dependency_overrides[getSession] = get_session_override
    with TestClient(app) as c:
        yield c
    # Clear the overrides after the test is done
    app.dependency_overrides.clear()

#Create a user for the mudule tests
@pytest.fixture(scope="module")
def user(client:TestClient):
    email = create_random_email()
    password = "GenericPassword1"
    response = client.post("/api/user",
                json={
                    "name": "Raul",
                    "lastName": "Garcia",
                    "secondLastName": "Pedrosa",
                    "dateOfBirth": "1991-09-11",
                    "nationalId": '23450045B',
                    "phone": "952751859",
                    "email": email,
                    "password": password
                })
    #assert response.status_code == 201
    print(response.json())
    return response.json()
@pytest.fixture(scope="module")
def user_token(client:TestClient,user:user):
    response = client.post("/api/token",
                           data={
                               "username": user["email"],
                               "password": "GenericPassword1"
                           })
    #assert response.status_code == 200
    print("Access token: " + response.json()["access_token"])
    return response.json()["access_token"]
