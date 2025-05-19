import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from unittest.mock import patch, MagicMock
from routes.aprendices_route import aprendices_router
from schemas.aprendices import Aprendices, ChangeStatusRequest
from jwt_manager import TokenData, verify_token

# Create a test FastAPI app
app = FastAPI()
app.include_router(aprendices_router)

# Create a function that will override the verify_token dependency
async def override_verify_token():
    return TokenData(document=123456789)

# Override the dependency
app.dependency_overrides[verify_token] = override_verify_token

# Create a test client
client = TestClient(app)

mock_aprendiz_data = {
    "name": "Test",
    "last_name": "Apprentice",
    "document": 123456789,
    "ficha": 1234567,
    "photo": "test_photo.jpg",
    "email": "test@example.com",
    "finish_date": "2025-12-31"
}

mock_aprendiz_response = {
    "id": 1,
    "name": "Test",
    "last_name": "Apprentice",
    "document": 123456789,
    "ficha": 1234567,
    "photo": "test_photo.jpg",
    "email": "test@example.com",
    "finish_date": "2025-12-31",
    "state_id": 1
}

mock_change_status_data = {
    "id": 123456789,
    "status_id": 2
}

@pytest.fixture
def mock_verify_token():
    yield

@patch("routes.aprendices_route.aprendices_service")
def test_get_user_all(mock_service, mock_verify_token):
    mock_service.get_all_aprendices.return_value = [mock_aprendiz_response]

    response = client.get("/api/v1/aprendices-all", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200
    assert response.json() == [mock_aprendiz_response]
    mock_service.get_all_aprendices.assert_called_once()

@patch("routes.aprendices_route.aprendices_service")
def test_create_aprendiz(mock_service):
    mock_service.create_aprendiz.return_value = {"message": "El aprendiz fue registrado exitosamente"}

    response = client.post("/api/v1/aprendiz-registration", json=mock_aprendiz_data)

    assert response.status_code == 200
    assert response.json() == {"message": "El aprendiz fue registrado exitosamente"}
    mock_service.create_aprendiz.assert_called_once()

@patch("routes.aprendices_route.aprendices_service")
def test_get_aprendiz_by_id(mock_service, mock_verify_token):
    mock_service.get_aprendiz_by_id.return_value = mock_aprendiz_response

    response = client.get("/api/v1/aprendices/id/document/1", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200
    assert response.json() == mock_aprendiz_response
    mock_service.get_aprendiz_by_id.assert_called_once_with(1)

@patch("routes.aprendices_route.aprendices_service")
def test_get_aprendiz_by_document(mock_service, mock_verify_token):
    mock_service.get_aprendiz_by_document.return_value = mock_aprendiz_response

    response = client.get("/api/v1/aprendices/123456789", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200
    assert response.json() == mock_aprendiz_response
    mock_service.get_aprendiz_by_document.assert_called_once_with(123456789)

@patch("routes.aprendices_route.aprendices_service")
def test_get_aprendiz_status_by_document(mock_service):
    mock_service.get_aprendiz_status_by_document.return_value = "Activo"

    response = client.get("/api/v1/aprendiz-status/123456789")

    assert response.status_code == 200
    assert response.json() == "Activo"
    mock_service.get_aprendiz_status_by_document.assert_called_once_with(123456789)

@patch("routes.aprendices_route.aprendices_service")
def test_change_aprendiz_status(mock_service, mock_verify_token):
    mock_service.change_aprendiz_status.return_value = {"message": "El estado del aprendiz fue actualizado correctamente"}

    response = client.put("/api/v1/aprendiz-change-status", json=mock_change_status_data, headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200
    assert response.json() == {"message": "El estado del aprendiz fue actualizado correctamente"}
    mock_service.change_aprendiz_status.assert_called_once()

@patch("routes.aprendices_route.aprendices_service")
def test_update_aprendiz(mock_service, mock_verify_token):
    mock_service.update_aprendiz.return_value = {"message": "El aprendiz fue actualizado correctamente"}

    response = client.put("/api/v1/aprendiz-update/123456789", json=mock_aprendiz_data, headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200
    assert response.json() == {"message": "El aprendiz fue actualizado correctamente"}
    # Check that update_aprendiz was called once with the document ID as the first argument
    # We don't check the exact second argument because FastAPI converts the JSON to an Aprendices object
    assert mock_service.update_aprendiz.call_count == 1
    args, _ = mock_service.update_aprendiz.call_args
    assert args[0] == 123456789
