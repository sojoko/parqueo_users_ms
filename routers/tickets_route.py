from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.tickets import Tickets
from models.tickets import Tickets as TicketsModel
from models.aprendices import Aprendices as AprendizModel
from models.users import User as UserModel



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
    get_tickets = db.query(TicketsModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(get_tickets))

@tickets_route.get("/api/v1/Ticket/id/{id}", tags=['Tickets'])
def get_ticket_by_id(id: int):
    db = Session()
    get_ticket_by_id = db.query(TicketsModel).filter(TicketsModel.id == id).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(get_ticket_by_id))