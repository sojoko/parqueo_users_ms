import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from unittest.mock import patch
from routes.vigilante_route import vigilante_router
from schemas.vigilantes import Vigilantes, ChangeStatusRequest
from jwt_manager import TokenData, verify_token

app = FastAPI()
app.include_router(vigilante_router)

async def override_verify_token():
    return TokenData(document=987654321)

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

mock_vigilante_data = {
    "name": "VigiTest",
    "last_name": "LanteTest",
    "document": 987654321
}

mock_vigilante_response = {
    'id': 1,
    'name': 'VigiTest',
    'last_name': 'LanteTest',
    'document': 987654321,
    'role_id': 3,  # Ajuste para coincidir con el servicio real
    'roll': 'vigilante'
}

mock_change_status_data = {
    "id": 1,
    "status_id": 2
}

@pytest.fixture
def mock_verify_token():
    yield

@patch("routes.vigilante_route.vigilante_service")
def test_create_vigilante(mock_service, mock_verify_token):
    mock_service.create_vigilante.return_value = {"message": "El usuario vigilante fue registrado correctamente"}
    response = client.post("/api/v1/vigilantes-registration", json=mock_vigilante_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El usuario vigilante fue registrado correctamente"

@patch("routes.vigilante_route.vigilante_service")
def test_update_vigilante(mock_service, mock_verify_token):
    mock_service.update_vigilante.return_value = {"message": "El usuario vigilante fue actualizado correctamente"}
    response = client.put("/api/v1/vigilantes-update/987654321", json=mock_vigilante_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El usuario vigilante fue actualizado correctamente"

@patch("routes.vigilante_route.vigilante_service")
def test_get_all_vigilant(mock_service, mock_verify_token):
    mock_service.get_all_vigilant.return_value = [mock_vigilante_response]
    response = client.get("/api/v1/vigilantes-all", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["roll"] == "vigilante"

@patch("routes.vigilante_route.vigilante_service")
def test_get_vigilante_by_document(mock_service, mock_verify_token):
    mock_service.get_vigilante_by_document.return_value = mock_vigilante_response
    response = client.get("/api/v1/vigilante/987654321", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["document"] == 987654321

@patch("routes.vigilante_route.vigilante_service")
def test_get_vigilante_by_id(mock_service, mock_verify_token):
    mock_service.get_vigilante_by_id.return_value = mock_vigilante_response
    response = client.get("/api/v1/vigilante-by-id/1", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routes.vigilante_route.vigilante_service")
def test_change_vigilante_status(mock_service, mock_verify_token):
    mock_service.change_vigilante_status.return_value = {"message": "El estado del vigilante fue actualizado correctamente"}
    response = client.put("/api/v1/vigilante-change-status", json=mock_change_status_data, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "El estado del vigilante fue actualizado correctamente"

