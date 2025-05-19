from datetime import datetime

from sqlalchemy import desc

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

    from typing import List, Dict, Any

    def get_tickets(self) -> List[Dict[str, Any]]:
        db: Session = Session()
        try:
            tickets = db.query(TicketsModel). \
                order_by(desc(TicketsModel.create_date)). \
                all()

            if not tickets:
                return []

            unique_documents = {t.document for t in tickets if t.document is not None}

            if not unique_documents:
                return []

            aprendices = db.query(AprendizModel).filter(AprendizModel.document.in_(unique_documents)).all()
            admins = db.query(AdminModel).filter(AdminModel.document.in_(unique_documents)).all()
            vigilantes = db.query(VigilanteModel).filter(VigilanteModel.document.in_(unique_documents)).all()

            aprendiz_dict = {a.document: a for a in aprendices}
            admin_dict = {a.document: a for a in admins}
            vigilante_dict = {v.document: v for v in vigilantes}

            ticket_data = []

            for ticket in tickets:
                user_info = None
                document = ticket.document

                if document in aprendiz_dict:
                    aprendiz = aprendiz_dict[document]
                    user_info = {
                        "name": aprendiz.name,
                        "last_name": aprendiz.last_name,
                        "type": "Aprendiz"
                    }
                elif document in admin_dict:
                    admin = admin_dict[document]
                    user_info = {
                        "name": admin.name,
                        "last_name": admin.last_name,
                        "type": "Admin"
                    }
                elif document in vigilante_dict:
                    vigilante = vigilante_dict[document]
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
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al obtener los tickets: {str(e)}")
        finally:
            db.close()

    def get_tickets_by_user(self, doc: int):
        db: Session = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == doc).first()
            if not aprendiz:
                return []

            tickets = db.query(TicketsModel). \
                filter(TicketsModel.document == doc). \
                order_by(desc(TicketsModel.create_date)). \
                all()
            ticket_data = []
            for ticket in tickets:
                ticket_info = {
                    "ticket_id": ticket.id,
                    "aprendiz_name": aprendiz.name + ' ' + aprendiz.last_name,
                    "ticket_description": ticket.description,
                    "status": ticket.status,
                    "create_date": ticket.create_date
                }
                ticket_data.append(ticket_info)
            return ticket_data

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al obtener los tickets: {str(e)}")
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