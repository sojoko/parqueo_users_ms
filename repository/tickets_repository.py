from datetime import datetime
from config.database import Session
from fastapi import HTTPException
from models.tickets import Tickets as TicketsModel
from models.aprendices import Aprendices as AprendizModel
from models.users import User as UserModel
from models.admins import Admins as AdminModel
from models.vigilantes import Vigilantes as VigilanteModel
from fastapi.encoders import jsonable_encoder

class TicketsRepository:
    def create_ticket(self, ticket_data: dict):
        db = Session()
        try:
            user = db.query(UserModel).filter(UserModel.document == ticket_data["document"]).first() 
            if not user:
                return None
                
            new_ticket = TicketsModel(**ticket_data, user_id=user.id)
            db.add(new_ticket)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
            
    def update_ticket(self, id: int, ticket_data: dict):
        db = Session()
        try:
            ticket = db.query(TicketsModel).filter(TicketsModel.id == id).first()
            if not ticket:
                return False

            for key, value in ticket_data.items():
                setattr(ticket, key, value)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")
        finally:
            db.close()
            
    def get_tickets(self):
        db = Session()
        try:
            tickets = db.query(TicketsModel).all()
            ticket_data = []

            for ticket in tickets:
                user_info = None

                # Buscar en AprendizModel
                aprendiz = db.query(AprendizModel).filter(AprendizModel.document == ticket.document).first()
                if aprendiz:
                    user_info = {
                        "name": aprendiz.name,
                        "last_name": aprendiz.last_name,
                        "type": "Aprendiz"
                    }

                # Buscar en AdminModel si no se encontró en AprendizModel
                if not user_info:
                    admin = db.query(AdminModel).filter(AdminModel.document == ticket.document).first()
                    if admin:
                        user_info = {
                            "name": admin.name,
                            "last_name": admin.last_name,
                            "type": "Admin"
                        }

                # Buscar en VigilanteModel si no se encontró en los anteriores
                if not user_info:
                    vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == ticket.document).first()
                    if vigilante:
                        user_info = {
                            "name": vigilante.name,
                            "last_name": vigilante.last_name,
                            "type": "Vigilante"
                        }

                if user_info:
                    ticket_info = {
                        "ticket_id": ticket.id,
                        "user_name": user_info["name"] + ' ' + user_info["last_name"],
                        "user_type": user_info["type"],
                        "ticket_description": ticket.description,
                        "status": ticket.status,
                        "create_date": ticket.create_date
                    }
                    ticket_data.append(ticket_info)

            return ticket_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
            
    def get_tickets_by_user(self, doc: int):
        db = Session()
        try:
            tickets = db.query(TicketsModel).filter(TicketsModel.document == doc)
            ticket_data = []
            for ticket in tickets:
                user = db.query(AprendizModel).filter(AprendizModel.document == ticket.document).first()
                if user:
                    ticket_info = {
                        "ticket_id": ticket.id,
                        "aprendiz_name": user.name + ' ' + user.last_name,
                        "ticket_description": ticket.description,
                        "status": ticket.status,
                        "create_date": ticket.create_date
                    }
                    ticket_data.append(ticket_info)
            return ticket_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
            
    def get_ticket_by_id(self, id: int):
        db = Session()
        try:
            ticket = db.query(TicketsModel).filter(TicketsModel.id == id).first()        
            return ticket
        except Exception as e:      
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()