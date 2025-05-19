import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from unittest.mock import patch
from routes.users_route import user_router
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
from jwt_manager import TokenData, verify_token

app = FastAPI()
app.include_router(user_router)

async def override_verify_token():
    return TokenData(document=123456789)

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

mock_user_data = {
    "document": 123456789,
    "password": "testpass"
}

mock_user_registry = {
    "document": 123456789,
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass",
    "roll_id": 2
}

mock_user_response = {
    "document": 123456789,
    "name": "Test User",
    "email": "test@example.com",
    "roll_id": 2
}

@patch("routes.users_route.users_service")
def test_get_user_route_success(mock_service):
    mock_service.get_user.return_value = mock_user_response
    response = client.get("/api/v1/users/123456789")
    assert response.status_code == 200
    assert response.json()["document"] == 123456789

@patch("routes.users_route.users_service")
def test_get_user_route_not_found(mock_service):
    mock_service.get_user.side_effect = HTTPException(status_code=404, detail="Usuario no encontrado")
    response = client.get("/api/v1/users/111")
    assert response.status_code == 404

@patch("routes.users_route.users_service")
def test_delete_user_route_success(mock_service):
    mock_service.delete_user.return_value = {"message": "Usuario eliminado con éxito"}
    response = client.delete("/api/v1/users/delete/123456789/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario eliminado con éxito"

@patch("routes.users_route.users_service")
def test_delete_user_route_not_found(mock_service):
    mock_service.delete_user.side_effect = HTTPException(status_code=404, detail="Usuario no encontrado")
    response = client.delete("/api/v1/users/delete/123456789/2")
    assert response.status_code == 404

@patch("routes.users_route.users_service")
def test_get_user_all_route_success(mock_service):
    mock_service.get_user_all.return_value = [mock_user_response]
    response = client.get("/api/v1/users_all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("routes.users_route.users_service")
def test_get_user_all_route_not_found(mock_service):
    mock_service.get_user_all.side_effect = HTTPException(status_code=404, detail="No se encontraron usuarios")
    response = client.get("/api/v1/users_all")
    assert response.status_code == 404

@patch("routes.users_route.users_service")
def test_login_route_success(mock_service):
    mock_service.login.return_value = {"access_token": "token", "token_type": "bearer"}
    response = client.post("/api/v1/login", json=mock_user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@patch("routes.users_route.users_service")
def test_login_route_fail(mock_service):
    mock_service.login.side_effect = HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    response = client.post("/api/v1/login", json=mock_user_data)
    assert response.status_code == 400

@patch("routes.users_route.users_service")
def test_create_user_route_success(mock_service):
    mock_service.create_user.return_value = {"message": "Usuario creado con éxito"}
    response = client.post("/api/v1/create_user", json=mock_user_registry)
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario creado con éxito"

@patch("routes.users_route.users_service")
def test_create_user_route_fail(mock_service):
    mock_service.create_user.side_effect = HTTPException(status_code=400, detail="Error al crear usuario")
    response = client.post("/api/v1/create_user", json=mock_user_registry)

