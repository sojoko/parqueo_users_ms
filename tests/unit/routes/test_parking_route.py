import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from unittest.mock import patch
from routes.parking import parking_router
from schemas.parking import Parking
from jwt_manager import TokenData, verify_token

app = FastAPI()
app.include_router(parking_router)

async def override_verify_token():
    return TokenData(document=123456789)

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

mock_parking_data = {
    "user_document": 123456789,
    "is_in_parking": 1,
    "vehicle_type": 1
}

@pytest.fixture
def mock_verify_token():
    yield

@patch("routes.parking.parking_service")
def test_create_parking(mock_service, mock_verify_token):
    mock_service.create_parking.return_value = {"message": "El movimiento fue regitrado correctamente"}
    response = client.post("/api/v1/parking-registration", json=mock_parking_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El movimiento fue regitrado correctamente"

@patch("routes.parking.parking_service")
def test_get_all_parking(mock_service, mock_verify_token):
    mock_service.get_all_parking.return_value = [mock_parking_data]
    response = client.get("/api/v1/parking-all", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("routes.parking.parking_service")
def test_get_all_parking_counter(mock_service, mock_verify_token):
    mock_service.get_all_parking_counter.return_value = 5
    response = client.get("/api/v1/parking-all-counter", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == 5

@patch("routes.parking.parking_service")
def test_get_parking_by_document(mock_service, mock_verify_token):
    mock_service.get_parking_by_document.return_value = mock_parking_data
    response = client.get("/api/v1/parking-by-document/123456789", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["user_document"] == 123456789

@patch("routes.parking.parking_service")
def test_update_parking(mock_service, mock_verify_token):
    mock_service.update_parking.return_value = {"message": "El registro de parqueo fue actualizado correctamente"}
    response = client.put("/api/v1/parking-registration-update/123456789", json=mock_parking_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El registro de parqueo fue actualizado correctamente"

