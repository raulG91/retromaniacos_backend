from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging


logger = logging.getLogger(__name__)

def test_add_event_participation(client: TestClient, user_token: str):
    logger.info("Starting test_add_event_participation")
    headers = {"Authorization": f"Bearer {user_token}"}
    # Create a new event to ensure there is an event to participate in
    response = client.post("/api/event",
                           json={
                                "name": "Retro Malaga",
                                "description": "Retro Malaga 2026" ,
                                "date": "2026-06-15",
                                "city": "Malaga"
                           },
                           headers=headers)
    assert response.status_code == 201
    event_id = response.json()["eventId"]
    # Now participate in the created event
    response = client.post(f"/api/participate/{event_id}", headers=headers)
    dict_json = response.json()
    assert response.status_code == 201 and dict_json["eventId"] == event_id

def test_get_event_participations(client: TestClient, user_token: str):
    logger.info("Starting test_get_event_participations")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create an event and participate in it to ensure there is at least one participation
    response = client.post("/api/event",
                           json={
                                 "name": "Test Event 2",
                                 "description": "This is a test event for participation",
                                 "date": "2026-06-01",
                                 "city": "Test City"
                            },
                            headers=headers)
    assert response.status_code == 201
    event_id = response.json()["eventId"]
    # Participate in the created event
    response = client.post(f"/api/participate/{event_id}", headers=headers)    
    assert response.status_code == 201                   
    response = client.get("/api/participations", headers=headers)
    assert response.status_code == 200
    participations = response.json()
    assert isinstance(participations, list)

def test_delete_event_participation(client: TestClient, user_token: str):
    logger.info("Starting test_delete_event_participation")
    headers = {"Authorization": f"Bearer {user_token}"}
    # Create an event and participate in it to ensure there is a participation to delete
    response = client.post("/api/event",
                           json={
                                 "name": "Test Event 3",
                                 "description": "This is a test event for participation deletion",
                                 "date": "2026-06-01",
                                 "city": "Test City"
                            },
                            headers=headers)
    assert response.status_code == 201
    event_id = response.json()["eventId"]
    # Participate in the created event
    response = client.post(f"/api/participate/{event_id}", headers=headers)    
    assert response.status_code == 201                   
    # Now delete the participation
    response = client.delete(f"/api/participate/{event_id}", headers=headers)
    assert response.status_code == 204    