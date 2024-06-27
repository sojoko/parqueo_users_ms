from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.tickets import Tickets
from models.tickets import Tickets as TicketsModel
from models.aprendices import Aprendices as AprendizModel
from models.users import User as UserModel
from models.admins import Admins as AdminModel
from models.vigilantes import Vigilantes as VigilanteModel



tickets_route = APIRouter()


@tickets_route.post("/api/v1/tickets-registration", tags=['Tickets'])
async def create_ticket(Tickets: Tickets):
    db = Session()
    user = db.query(UserModel).filter(UserModel.document == Tickets.document).first() 
    try:       
     
        Tickets.document = int(Tickets.document)
        new_ticket = TicketsModel(
            document=Tickets.document,   
            user_id=user.id,       
            vehicle_type=Tickets.vehicle_type,
            placa=Tickets.placa,
            numero_marco=Tickets.numero_marco,
            date=Tickets.date,
            description=Tickets.description,
            photo=Tickets.photo,
            status=Tickets.status         
                          
        )
        db.add(new_ticket)
        db.commit()
        return {"message": "El ticket se creo exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

# -----------------------------------------------------------------------------------------
    
@tickets_route.put("/api/v1/ticket-response/{id}", tags=['Tickets'])
async def update_ticket(id: int, Tickets: Tickets):
    db = Session()
    try:
        ticket = db.query(TicketsModel).filter(TicketsModel.id == id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.status = Tickets.status
        ticket.response_subject = Tickets.response_subject
        ticket.response_body = Tickets.response_body
        
        db.commit()
        
        return {"message": "Ticket updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")
    finally:
        db.close()

#   --------------------------------------------------------------------------------------------    

@tickets_route.get("/api/v1/Tickets", tags=['Tickets'])
def get_tickets():
    db = Session()
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

    return JSONResponse(status_code=200, content=jsonable_encoder(ticket_data))


# ----------------------------------------------------------------------------------------------------

@tickets_route.get("/api/v1/Tickets-by-user/{doc}", tags=['Tickets'])
def get_tickets_by_user(doc: int):
    db = Session()
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
    return JSONResponse(status_code=200, content=jsonable_encoder(ticket_data))

# ----------------------------------------------------------------------------------------------------

@tickets_route.get("/api/v1/Ticket/id/{id}", tags=['Tickets'])
def get_ticket_by_id(id: int):
    db = Session()
    get_ticket_by_id = db.query(TicketsModel).filter(TicketsModel.id == id).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(get_ticket_by_id))