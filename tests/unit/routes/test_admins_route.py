import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from unittest.mock import patch, MagicMock
from routes.admins_route import admins_router
from schemas.admins import Admins, ChangeStatusRequest
from jwt_manager import TokenData, verify_token

app = FastAPI()
app.include_router(admins_router)

async def override_verify_token():
    return TokenData(document=987654321)

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

mock_admin_data = {
    "name": "AdminTest",
    "last_name": "AdminLast",
    "document": 987654321
}

mock_admin_response = {
    "id": 1,
    "name": "AdminTest",
    "last_name": "AdminLast",
    "document": 987654321,
    "roll": "admin"
}

mock_change_status_data = {
    "id": 1,
    "status_id": 2
}

@pytest.fixture
def mock_verify_token():
    yield

@patch("routes.admins_route.admins_service")
def test_create_admin(mock_service, mock_verify_token):
    mock_service.create_admin.return_value = {"message": "El usuario Admin fue regitrado correctamente"}
    response = client.post("/api/v1/admins-registration", json=mock_admin_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El usuario Admin fue regitrado correctamente"

@patch("routes.admins_route.admins_service")
def test_get_all_admins(mock_service, mock_verify_token):
    mock_service.get_all_admins.return_value = [mock_admin_response]
    response = client.get("/api/v1/admins-all", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1

@patch("routes.admins_route.admins_service")
def test_update_admin(mock_service, mock_verify_token):
    mock_service.update_admin.return_value = {"message": "El usuario administrador fue actualizado correctamente"}
    response = client.put("/api/v1/admins-update/1", json=mock_admin_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El usuario administrador fue actualizado correctamente"

@patch("routes.admins_route.admins_service")
def test_get_admin_by_id(mock_service, mock_verify_token):
    mock_service.get_admin_by_id.return_value = mock_admin_response
    response = client.get("/api/v1/admin-by-id/1", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routes.admins_route.admins_service")
def test_change_admin_status(mock_service, mock_verify_token):
    mock_service.change_admin_status.return_value = {"message": "El estado del administrador fue actualizado correctamente"}
    response = client.put("/api/v1/admin-change-status", json=mock_change_status_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El estado del administrador fue actualizado correctamente"

