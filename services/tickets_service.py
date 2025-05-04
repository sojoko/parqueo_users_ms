from datetime import datetime, timedelta
from fastapi import HTTPException, status
from schemas.tickets import Tickets
from repository.tickets_repository import TicketsRepository

class TicketsService:
    def __init__(self):
        self.repository = TicketsRepository()
    def create_ticket(self, tickets: Tickets):
        try:       
            tickets.document = int(tickets.document)

            ticket_data = {
                "document": tickets.document,
                "vehicle_type": tickets.vehicle_type,
                "placa": tickets.placa,
                "numero_marco": tickets.numero_marco,
                "date": tickets.date,
                "description": tickets.description,
                "photo": tickets.photo,
                "status": tickets.status
            }

            result = self.repository.create_ticket(ticket_data)

            if result is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            return {"message": "El ticket se creo exitosamente."}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def update_ticket(self, id: int, tickets: Tickets):
        try:
            ticket_data = {
                "status": tickets.status,
                "response_subject": tickets.response_subject,
                "response_body": tickets.response_body
            }

            success = self.repository.update_ticket(id, ticket_data)

            if not success:
                raise HTTPException(status_code=404, detail="Ticket not found")

            return {"message": "Ticket updated successfully"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")

    def get_tickets(self):
        try:
            return self.repository.get_tickets()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_tickets_by_user(self, doc: int):
        try:
            return self.repository.get_tickets_by_user(doc)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_ticket_by_id(self, id: int):
        try:
            ticket = self.repository.get_ticket_by_id(id)        
            if ticket is None:
                raise HTTPException(status_code=404, detail="El ticket no fue encontrado")        
            return ticket
        except HTTPException as http_exc:      
            raise http_exc
        except Exception as e:      
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
