import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from services.tickets_service import TicketsService
from schemas.tickets import Tickets

# Mock data para las pruebas
mock_ticket_data = Tickets(
    document="123456789",
    vehicle_type="Motocicleta",
    placa="ABC123",
    numero_marco="12345678901234567",
    date="2025-05-18",
    description="Rayón en el tanque de la motocicleta",
    photo="https://example.com/foto.jpg",
    status=1
)

mock_ticket_response = {
    'id': 1,
    'user_id': 10,
    'document': 123456789,
    'vehicle_type': 'Motocicleta',
    'placa': 'ABC123',
    'numero_marco': '12345678901234567',
    'date': '2025-05-18',
    'description': 'Rayón en el tanque de la motocicleta',
    'photo': 'https://example.com/foto.jpg',
    'status': 1,
    'create_date': '2025-05-18T10:00:00',
    'response_subject': None,
    'response_body': None
}

mock_update_ticket_data = Tickets(
    status=2,
    response_subject="Respuesta a su ticket",
    response_body="Su caso ha sido procesado correctamente."
)

class TestTicketsService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = TicketsService(repository=self.mock_repo)

    def test_create_ticket_success(self):
        self.mock_repo.create_ticket.return_value = True
        result = self.service.create_ticket(mock_ticket_data)
        assert result["message"] == "El ticket se creo exitosamente."

    def test_create_ticket_user_not_found(self):
        self.mock_repo.create_ticket.return_value = None
        with pytest.raises(HTTPException) as exc:
            self.service.create_ticket(mock_ticket_data)
        assert exc.value.status_code == 404
        assert "Usuario no encontrado" in exc.value.detail

    def test_update_ticket_success(self):
        self.mock_repo.update_ticket.return_value = True
        result = self.service.update_ticket(1, mock_update_ticket_data)
        assert result["message"] == "Ticket updated successfully"

    def test_update_ticket_not_found(self):
        self.mock_repo.update_ticket.return_value = False
        with pytest.raises(HTTPException) as exc:
            self.service.update_ticket(999, mock_update_ticket_data)
        assert exc.value.status_code == 404
        assert "Ticket not found" in exc.value.detail

    def test_get_tickets(self):
        self.mock_repo.get_tickets.return_value = [mock_ticket_response]
        result = self.service.get_tickets()
        assert isinstance(result, list)
        assert result[0]['id'] == 1
        assert result[0]['vehicle_type'] == 'Motocicleta'

    def test_get_tickets_by_user_success(self):
        self.mock_repo.get_tickets_by_user.return_value = [mock_ticket_response]
        result = self.service.get_tickets_by_user(123456789)
        assert isinstance(result, list)
        assert result[0]['document'] == 123456789
        assert result[0]['vehicle_type'] == 'Motocicleta'

    def test_get_tickets_by_user_not_found(self):
        self.mock_repo.get_tickets_by_user.return_value = []
        with pytest.raises(HTTPException) as exc:
            self.service.get_tickets_by_user(999999)
        assert exc.value.status_code == 404
        assert "No se encontraron tickets para este usuario" in exc.value.detail

    def test_get_ticket_by_id_success(self):
        self.mock_repo.get_ticket_by_id.return_value = mock_ticket_response
        result = self.service.get_ticket_by_id(1)
        assert result['id'] == 1
        assert result['placa'] == 'ABC123'

    def test_get_ticket_by_id_not_found(self):
        self.mock_repo.get_ticket_by_id.return_value = None
        with pytest.raises(HTTPException) as exc:
            self.service.get_ticket_by_id(999)
        assert exc.value.status_code == 404
        assert "El ticket no fue encontrado" in exc.value.detail
