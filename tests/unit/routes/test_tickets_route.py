import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException
from unittest.mock import patch
from routes.tickets_route import tickets_route
from schemas.tickets import Tickets
from jwt_manager import TokenData, verify_token

app = FastAPI()
app.include_router(tickets_route)

async def override_verify_token():
    return TokenData(document=123456789)

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

# Mock data para las pruebas
mock_ticket_data = {
    "document": "123456789",
    "vehicle_type": "Motocicleta",
    "placa": "ABC123",
    "numero_marco": "12345678901234567",
    "date": "2025-05-18",
    "description": "Rayón en el tanque de la motocicleta",
    "photo": "https://example.com/foto.jpg",
    "status": 1
}

mock_update_ticket_data = {
    "status": 2,
    "response_subject": "Respuesta a su ticket",
    "response_body": "Su caso ha sido procesado correctamente."
}

@pytest.fixture
def mock_verify_token():
    yield

@patch("routes.tickets_route.tickets_service")
def test_create_ticket_route_success(mock_service, mock_verify_token):
    mock_service.create_ticket.return_value = {"message": "El ticket se creo exitosamente."}
    response = client.post("/api/v1/tickets-registration", json=mock_ticket_data)
    assert response.status_code == 200
    assert response.json()["message"] == "El ticket se creo exitosamente."

@patch("routes.tickets_route.tickets_service")
def test_create_ticket_route_failure(mock_service, mock_verify_token):
    mock_service.create_ticket.side_effect = HTTPException(status_code=404, detail="Usuario no encontrado")
    response = client.post("/api/v1/tickets-registration", json=mock_ticket_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

@patch("routes.tickets_route.tickets_service")
def test_update_ticket_route_success(mock_service, mock_verify_token):
    mock_service.update_ticket.return_value = {"message": "Ticket updated successfully"}
    response = client.put("/api/v1/ticket-response/1", json=mock_update_ticket_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket updated successfully"

@patch("routes.tickets_route.tickets_service")
def test_update_ticket_route_not_found(mock_service, mock_verify_token):
    mock_service.update_ticket.side_effect = HTTPException(status_code=404, detail="Ticket not found")
    response = client.put("/api/v1/ticket-response/999", json=mock_update_ticket_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"

@patch("routes.tickets_route.tickets_service")
def test_get_tickets_route(mock_service, mock_verify_token):
    mock_ticket_response = {
        'id': 1,
        'vehicle_type': 'Motocicleta',
        'placa': 'ABC123'
    }
    mock_service.get_tickets.return_value = [mock_ticket_response]
    response = client.get("/api/v1/Tickets")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['vehicle_type'] == 'Motocicleta'

@patch("routes.tickets_route.tickets_service")
def test_get_tickets_by_user_route_success(mock_service, mock_verify_token):
    mock_ticket_response = {
        'id': 1,
        'document': 123456789,
        'vehicle_type': 'Motocicleta'
    }
    mock_service.get_tickets_by_user.return_value = [mock_ticket_response]
    response = client.get("/api/v1/Tickets-by-user/123456789")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['document'] == 123456789

@patch("routes.tickets_route.tickets_service")
def test_get_tickets_by_user_route_not_found(mock_service, mock_verify_token):
    from fastapi import HTTPException
    mock_service.get_tickets_by_user.side_effect = HTTPException(status_code=404, detail="No se encontraron tickets")
    response = client.get("/api/v1/Tickets-by-user/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No se encontraron tickets"

@patch("routes.tickets_route.tickets_service")
def test_get_ticket_by_id_route_success(mock_service, mock_verify_token):
    mock_ticket_response = {
        'id': 1,
        'placa': 'ABC123',
        'vehicle_type': 'Motocicleta'
    }
    mock_service.get_ticket_by_id.return_value = mock_ticket_response
    response = client.get("/api/v1/Ticket/id/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['placa'] == 'ABC123'

@patch("routes.tickets_route.tickets_service")
def test_get_ticket_by_id_route_not_found(mock_service, mock_verify_token):
    from fastapi import HTTPException
    mock_service.get_ticket_by_id.side_effect = HTTPException(status_code=404, detail="Ticket no encontrado")
    response = client.get("/api/v1/Ticket/id/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket no encontrado"
