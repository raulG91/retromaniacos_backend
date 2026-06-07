from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging


logger = logging.getLogger(__name__)

def test_create_material(client:TestClient,user_token:str):
    '''Test creation of a material'''
    logger.info("Starting test_create_material")
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/material",
                           json={
                               "name": "Game Test",
                               "description": "This is a test game",
                               "type": "Game"
                           },
                            headers=headers)
    dict_json = response.json()
    logger.info(f'Response from /api/material: {dict_json}')
    assert response.status_code == 201 and dict_json["name"] == "Game Test" and dict_json["description"] == "This is a test game" and dict_json["type"] == "Game"

def test_get_materials(client:TestClient,user_token:str):
    logger.info("Starting test_get_materials")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new material to ensure there is at least one material to retrieve
    response = client.post("/api/material",
                           json={
                               "name": "Sony Triniton",
                               "description": "A classic CRT monitor",
                               "type": "TV"
                           },
                           headers=headers)
    response = client.get("/api/material", headers=headers)
    dict_json = response.json()
    assert response.status_code == 200
    for material in dict_json:
        assert "name" in material and "description" in material and "type" in material                       

def test_delete_material(client: TestClient,user_token:str):
    logger.debug("Starting test delete material")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new material to ensure there is a material to delete
    response=client.post("/api/material",
                json={
                    "name": "Material to delete",
                    "description": "This material will be deleted",
                    "type": "Game"
                },
                headers=headers)
    mateialId = response.json()["materialId"]
    response = client.delete(f"/api/material/{mateialId}", headers=headers)
    assert response.status_code == 204

def test_update_material(client: TestClient,user_token:str):
    logger.info("Starting test_update_material")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new material to ensure there is a material to update
    response = client.post("/api/material",
                           json={
                               "name": "Material to update",
                               "description": "This material will be updated",
                               "type": "Game"
                           },
                           headers=headers)
    assert response.status_code == 201
    materialId = response.json()["materialId"]
    response = client.patch(f"/api/material/{materialId}",
                            json={
                                "name": "Updated Material",
                                "description": "This material has been updated",
                                "type": "Console"
                            },
                            headers=headers)
    dict_json = response.json()
    assert response.status_code == 200 and dict_json["name"] == "Updated Material" and dict_json["description"] == "This material has been updated" and dict_json["type"] == "Console"

def test_replace_material(client:TestClient,user_token: str):
    logger.info("Starting test replace material")
    headers = {"Authorization": f"Bearer {user_token}"}
    #Create a new material to ensure there is a material to replace
    response = client.post("/api/material", 
                           json={
                               "name": "Material to replace",
                               "description": "This material will be replaced",
                               "type": "Game"
                           },
                           headers=headers)
    assert response.status_code == 201
    materialId = response.json()["materialId"]
    response = client.put(f'/api/material/{materialId}',
                          json={
                              "name": "Replaced Material",
                              "description": "This material has been replaced",
                              "type": "TV"
                          },
                          headers=headers
                        )
    response_dict = response.json()
    assert response.status_code == 200 and response_dict["name"] == "Replaced Material" and response_dict["description"] == "This material has been replaced" and response_dict["type"] == "TV"
