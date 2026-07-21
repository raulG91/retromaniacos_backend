from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging

logger = logging.getLogger(__name__)

def test_add_event_material(client: TestClient, user_token:str):
    logger.info("Starting test_add_event_material")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new event and a new material to ensure there is an event to add material to
    response = client.post("/api/event",
                           json={
                                "name": "Retro Test",
                                "description": "Retro Test 2026" ,
                                "date": "2026-06-15",
                                "city": "Malaga"
                           },
                           headers=headers)
    assert response.status_code == 201
    event_id = response.json()["eventId"]

    response = client.post("/api/material",
                           json={
                                "name": "Test Game",
                                "description": "Test Game description",
                                "type": "Game"
                           },
                           headers=headers)
    assert response.status_code == 201
    material_id = response.json()["materialId"]
    #Add material to event
    response = client.post(f"/api/event/{event_id}/material/{material_id}", headers=headers)
    assert response.status_code == 201

def test_get_event_material(client: TestClient, user_token:str):

    #Add the event and material first to ensure there is something to retrieve
    test_add_event_material(client, user_token)  # Ensure there is an event and material to retrieve
    logger.info("Starting test_get_event_material")
    response = client.get("/api/event/1/material", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200

def test_delete_event_material(client: TestClient, user_token: str):
    #Add the event and material first to ensure there is something to delete
    logger.info("Starting test_add_event_material")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new event and a new material to ensure there is an event to add material to
    response = client.post("/api/event",
                           json={
                                "name": "Retro Test",
                                "description": "Retro Test 2026" ,
                                "date": "2026-06-15",
                                "city": "Malaga"
                           },
                           headers=headers)
    assert response.status_code == 201
    event_id = response.json()["eventId"]

    response = client.post("/api/material",
                           json={
                                "name": "Test Game",
                                "description": "Test Game description",
                                "type": "Game"
                           },
                           headers=headers)
    assert response.status_code == 201
    material_id = response.json()["materialId"]
    #Add material to event
    response = client.post(f"/api/event/{event_id}/material/{material_id}", headers=headers)
    assert response.status_code == 201
    #Now delete the material from the event
    response = client.delete(f"/api/event/{event_id}/material/{material_id}", headers=headers)
    assert response.status_code == 204
    