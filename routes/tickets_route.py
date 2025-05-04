from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.tickets import Tickets
from fastapi import Request
from services.tickets_service import TicketsService


tickets_route = APIRouter()
tickets_service = TicketsService()

@limiter.limit("20/minute")
@tickets_route.post("/api/v1/tickets-registration", tags=['Tickets'])
async def create_ticket(request:Request, tickets: Tickets, token: TokenData = Depends(verify_token)):
    result = tickets_service.create_ticket(tickets)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# -----------------------------------------------------------------------------------------


@limiter.limit("20/minute")
@tickets_route.put("/api/v1/ticket-response/{id}", tags=['Tickets'])
async def update_ticket(request:Request, id: int, tickets: Tickets, token: TokenData = Depends(verify_token)):
    result = tickets_service.update_ticket(id, tickets)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#   --------------------------------------------------------------------------------------------    
@limiter.limit("20/minute")
@tickets_route.get("/api/v1/Tickets", tags=['Tickets'])
def get_tickets(request:Request, token: TokenData = Depends(verify_token)):
    ticket_data = tickets_service.get_tickets()
    return JSONResponse(status_code=200, content=jsonable_encoder(ticket_data))


# ----------------------------------------------------------------------------------------------------
@limiter.limit("20/minute")
@tickets_route.get("/api/v1/Tickets-by-user/{doc}", tags=['Tickets'])
def get_tickets_by_user(request:Request, doc: int, token: TokenData = Depends(verify_token)):
    ticket_data = tickets_service.get_tickets_by_user(doc)
    return JSONResponse(status_code=200, content=jsonable_encoder(ticket_data))

# ----------------------------------------------------------------------------------------------------

@tickets_route.get("/api/v1/Ticket/id/{id}", tags=['Tickets'])
def get_ticket_by_id(request:Request, id: int, token: TokenData = Depends(verify_token)):
    ticket = tickets_service.get_ticket_by_id(id)
    return JSONResponse(status_code=200, content=jsonable_encoder(ticket))
