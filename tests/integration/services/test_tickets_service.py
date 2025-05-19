import pytest
from fastapi import HTTPException
from services.tickets_service import TicketsService
from schemas.tickets import Tickets
from config.database import Session
from models.tickets import Tickets as TicketsModel
from models.users import User as UserModel
from models.aprendices import Aprendices as AprendizModel
import datetime

# Test data for integration tests
test_ticket_data = Tickets(
    document="123456789",
    vehicle_type="Motocicleta",
    placa="ABC123",
    numero_marco="12345678901234567",
    date=datetime.datetime.now().strftime("%Y-%m-%d"),
    description="Rayón en el tanque de la motocicleta - Integration Test",
    photo="https://example.com/foto_integration.jpg",
    status=1
)

test_update_ticket_data = Tickets(
    status=2,
    response_subject="Respuesta a su ticket - Integration Test",
    response_body="Su caso ha sido procesado correctamente en prueba de integración."
)

class TestTicketsServiceIntegration:
    """
    Integration tests for TicketsService.
    These tests use the actual database connection instead of mocks.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Setup before each test and cleanup after each test.
        """
        # Setup - ensure test user and aprendiz exist
        self.service = TicketsService()
        self.db = Session()

        # Store created test data for cleanup
        self.created_ticket_ids = []
        self.created_test_user = False
        self.created_test_aprendiz = False

        # Check if test user exists, create if not
        test_user = self.db.query(UserModel).filter(UserModel.document == 123456789).first()
        if not test_user:
            test_user = UserModel(document=123456789, password="2020", state_id=1, roll_id=2)
            self.db.add(test_user)
            self.db.commit()
            self.created_test_user = True

        self.test_user_id = test_user.id

        # Check if test aprendiz exists, create if not
        test_aprendiz = self.db.query(AprendizModel).filter(AprendizModel.document == 123456789).first()
        if not test_aprendiz:
            test_aprendiz = AprendizModel(
                document=123456789,
                name="Test",
                last_name="Aprendiz",
                ficha=12345,
                email="test.aprendiz@example.com",
                photo="https://example.com/photo.jpg",
                status_id=1
            )
            self.db.add(test_aprendiz)
            self.db.commit()
            self.created_test_aprendiz = True

        self.test_aprendiz_id = test_aprendiz.id

        yield  # This is where the test runs

        # Teardown - clean up test data
        for ticket_id in self.created_ticket_ids:
            ticket = self.db.query(TicketsModel).filter(TicketsModel.id == ticket_id).first()
            if ticket:
                self.db.delete(ticket)

        # Clean up test user and aprendiz if they were created during this test
        if self.created_test_user:
            user = self.db.query(UserModel).filter(UserModel.id == self.test_user_id).first()
            if user:
                self.db.delete(user)

        if self.created_test_aprendiz:
            aprendiz = self.db.query(AprendizModel).filter(AprendizModel.id == self.test_aprendiz_id).first()
            if aprendiz:
                self.db.delete(aprendiz)

        self.db.commit()
        self.db.close()

    def test_create_ticket_integration(self):
        """Test creating a ticket with real database connection."""
        result = self.service.create_ticket(test_ticket_data)

        # Verify ticket was created
        assert result["message"] == "El ticket se creo exitosamente."

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Find the created ticket for cleanup
        ticket = self.db.query(TicketsModel).filter(
            TicketsModel.document == 123456789,
            TicketsModel.description == "Rayón en el tanque de la motocicleta - Integration Test"
        ).first()

        assert ticket is not None
        assert ticket.vehicle_type == "Motocicleta"
        assert ticket.placa == "ABC123"

        # Store for cleanup
        self.created_ticket_ids.append(ticket.id)

    def test_update_ticket_integration(self):
        """Test updating a ticket with real database connection."""
        # First create a ticket
        self.service.create_ticket(test_ticket_data)

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Find the created ticket
        ticket = self.db.query(TicketsModel).filter(
            TicketsModel.document == 123456789,
            TicketsModel.description == "Rayón en el tanque de la motocicleta - Integration Test"
        ).first()

        assert ticket is not None
        self.created_ticket_ids.append(ticket.id)

        # Verify initial status
        assert ticket.status == 1
        print(f"Initial ticket status: {ticket.status}")

        # Create a new ticket object with the updated status
        update_data = Tickets(
            status=2,
            response_subject="Respuesta a su ticket - Integration Test",
            response_body="Su caso ha sido procesado correctamente en prueba de integración."
        )

        # Update the ticket
        result = self.service.update_ticket(ticket.id, update_data)

        # Verify update was successful
        assert result["message"] == "Ticket updated successfully"

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Get the ticket again from the database
        updated_ticket = self.db.query(TicketsModel).filter(TicketsModel.id == ticket.id).first()
        print(f"Updated ticket status: {updated_ticket.status}")

        # Verify the ticket was updated in the database
        assert updated_ticket.status == 2, f"Expected status to be 2, but got {updated_ticket.status}"
        assert updated_ticket.response_subject == "Respuesta a su ticket - Integration Test"
        assert updated_ticket.response_body == "Su caso ha sido procesado correctamente en prueba de integración."

    def test_get_tickets_integration(self):
        """Test getting all tickets with real database connection."""
        # First create a ticket
        self.service.create_ticket(test_ticket_data)

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Find the created ticket
        ticket = self.db.query(TicketsModel).filter(
            TicketsModel.document == 123456789,
            TicketsModel.description == "Rayón en el tanque de la motocicleta - Integration Test"
        ).first()

        assert ticket is not None
        self.created_ticket_ids.append(ticket.id)

        # Get all tickets
        tickets = self.service.get_tickets()

        # Verify we got tickets back
        assert isinstance(tickets, list)
        assert len(tickets) > 0

    def test_get_tickets_by_user_integration(self):
        """Test getting tickets by user with real database connection."""
        # First create a ticket
        self.service.create_ticket(test_ticket_data)

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Find the created ticket
        ticket = self.db.query(TicketsModel).filter(
            TicketsModel.document == 123456789,
            TicketsModel.description == "Rayón en el tanque de la motocicleta - Integration Test"
        ).first()

        assert ticket is not None
        self.created_ticket_ids.append(ticket.id)

        # Get tickets by user
        tickets = self.service.get_tickets_by_user(123456789)

        # Verify we got tickets back
        assert isinstance(tickets, list)
        assert len(tickets) > 0

        # Verify the ticket belongs to our test user
        found = False
        for t in tickets:
            if t["ticket_id"] == ticket.id:
                found = True
                break

        assert found, "Created ticket not found in user's tickets"

    def test_get_ticket_by_id_integration(self):
        """Test getting a ticket by ID with real database connection."""
        # First create a ticket
        self.service.create_ticket(test_ticket_data)

        # Close and reopen the session to ensure we get the latest data
        self.db.close()
        self.db = Session()

        # Find the created ticket
        ticket = self.db.query(TicketsModel).filter(
            TicketsModel.document == 123456789,
            TicketsModel.description == "Rayón en el tanque de la motocicleta - Integration Test"
        ).first()

        assert ticket is not None
        self.created_ticket_ids.append(ticket.id)

        # Get ticket by ID
        result = self.service.get_ticket_by_id(ticket.id)

        # Verify we got the right ticket
        assert result is not None
        assert result.id == ticket.id
        assert result.document == 123456789
        assert result.vehicle_type == "Motocicleta"
        assert result.placa == "ABC123"
