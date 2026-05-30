from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging
from .test_util import create_random_email

#Initialize logger 
logger = logging.getLogger(__name__)

def test_create_event(client: TestClient,user_token:str):
    '''Test the creation of an event'''
    logger.info("Starting test_create_event")
    assert user_token is not None
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/event", 
                            json={
                                "name": "Event Test",
                                "description": "This is a test event",
                                "date": "2026-06-01",
                                "city": "Test City"
                            },
                            headers=headers)
    dict_json = response.json()
    logger.info(f"Response from /api/event: {dict_json}")
    assert response.status_code == 201 and dict_json["name"] == "Event Test"

def test_get_events(client: TestClient,user_token: str):
    logger.info("Starting test_get_events")
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/event", headers=headers)
    dict_json= response.json()
    assert response.status_code == 200
    for event in dict_json:
        assert "name" in event and "description" in event and "date" in event and "city" in event

def test_update_event(client: TestClient, user_token:str):
    logger.info("Starting test_update_event")
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/event",
                           json={
                                "name": "Event Test to Update",
                                "description": "This is a test event to update",
                                "date": "2026-06-01",
                                "city": "Test City"
                             },
                            headers=headers)
    dict_json= response.json()
    assert response.status_code == 201
    event_id = dict_json["eventId"]
    response = client.patch(f'/api/event/{event_id}', 
                            json={
                                "name": "Event Test Updated",
                                "description": "This is an updated test event",
                                "date": "2026-06-02",
                                "city": "Updated Test City"
                            },
                            headers=headers)
    response_json = response.json()
    assert response.status_code == 200 and response_json["name"] == "Event Test Updated" and response_json["description"] == "This is an updated test event" and response_json["date"] == "2026-06-02" and response_json["city"] == "Updated Test City"

def test_delete_event(client: TestClient, user_token:str):
    logger.info("Starting test_delete_event")
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/event", 
                            json={
                                "name": "Event Test to Delete",
                                "description": "This is a test event to delete",
                                "date": "2026-06-03",
                                "city": "Test City"
                            },
                            headers=headers)
    dict_json = response.json()
    assert response.status_code == 201 
    response = client.delete(f'/api/event/{dict_json["eventId"]}', headers=headers)
    assert response.status_code == 204

def test_replace_event(client: TestClient, user_token:str):
    logger.info("Starting test_replace_event")
    headers  = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/event",
                           json={
                                "name": "Event Test to Replace",
                                "description": "This is a test event to replace",
                                "date": "2026-06-01",
                                "city": "Test City"
                             },
                            headers=headers)
    dict_json= response.json()
    event_id = dict_json["eventId"]
    response = client.put(f'/api/event/{event_id}', 
                            json={
                                "name": "Event Test Replaced",
                                "description": "This is a replaced test event",
                                "date": "2026-06-04",
                                "city": "Replaced Test City",
                                "street": "Replaced Test Street",
                                "zipCode": 12344,
                                "autoOrganized": False
                            },
                            headers=headers)
    response_json = response.json()
    logger.info(f"Response from /api/event/{event_id}: {response_json}")
    assert response.status_code == 200 and response_json["name"] == "Event Test Replaced" and response_json["description"] == "This is a replaced test event" and response_json["date"] == "2026-06-04" and response_json["city"] == "Replaced Test City" and response_json["street"] == "Replaced Test Street" and response_json["zipCode"] == 12344 and response_json["autoOrganized"] == False