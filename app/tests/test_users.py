from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging
from .test_util import create_random_email

#Initialize logger 
logger = logging.getLogger(__name__)


def test_get_user_data(client: TestClient,user_token:str):
    '''Test get user data'''
    assert user_token is not None
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/user/me", headers=headers)
    dict_json = response.json()
    logger.info(f"Response from /api/user/me: {dict_json}")
    assert response.status_code == 200 and dict_json["name"].lower() == "Raul".lower()


def test_user_update(client: TestClient,user,user_token:str):
    '''Test the update of user data'''
    header = {"Authorization": f"Bearer {user_token}"}
    response = client.put("/api/user/me", 
                          json={"name": user["name"]+"Updated",
                                "lastName": user["lastName"]+"Updated",
                                "secondLastName": user["secondLastName"]+"Updated",
                                "dateOfBirth": user["dateOfBirth"],
                                "phone": user["phone"],
                                "nationalId": user["nationalId"],
                                "email": user["email"]
                            }, 
                          headers=header)
    dict_json = response.json()
    assert response.status_code == 200 and dict_json["name"] == user["name"]+"Updated".lower() and dict_json["lastName"] == user["lastName"]+"Updated".lower() and dict_json["secondLastName"] == user["secondLastName"]+"Updated".lower()

def test_user_password_uptade(client:TestClient):
    '''Test the update of user password'''
    email = create_random_email()
    password = "GenericPassword1"
    #Create a user
    response = client.post("/api/user",
                json={
                    "name": "Raul",
                    "lastName": "Garcia",
                    "secondLastName": "Pedrosa",
                    "dateOfBirth": "1991-09-11",
                    "nationalId": '23450045B',
                    "email": email,
                    "phone": "658987564",
                    "password": password
                })
    assert response.status_code == 201
    #Login with the created user
    response = client.post("/api/token",
                            data={
                                "username": email,
                                "password": password
                            })
    assert response.status_code == 200
    token = response.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    #Update the password
    response = client.patch("/api/user/me/password", 
                          json={"password": "NewGenericPassword1"
                            }, 
                          headers=header)
    assert response.status_code == 200

    #User is able to login with the new password    
    response = client.post("/api/token",
                            data={
                                "username": email,
                                "password": "NewGenericPassword1"
                            })
    assert response.status_code == 200

def test_user_deletion(client:TestClient,user_token:str):
    
    '''Test the deletion of user'''
    header = {"Authorization": f"Bearer {user_token}"}
    response = client.delete("/api/user/me", headers=header)
    assert response.status_code == 204
