from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from models.parking import Parking as ParkingModel
from schemas.parking import Parking
from fastapi import Depends, HTTPException, status
from fastapi import Request



parking_router = APIRouter()

@limiter.limit("30/minute")
@parking_router.post("/api/v1/parking-registration", tags=['parking'])
async def create_parking(request:Request, parking : Parking, token: TokenData = Depends(verify_token)):
    db = Session()
    parking.user_document = int(parking.user_document)
    
    user_exist = db.query(ParkingModel).filter(ParkingModel.user_document == parking.user_document).first()
    if user_exist:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un registro para este usuario en el parqueadero",
            )
    try:       
        new_paking = ParkingModel(
            user_document=parking.user_document,
            is_in_parking=parking.is_in_parking,
            vehicle_type=parking.vehicle_type                                   
        )
        db.add(new_paking)
        db.commit()
        return {"message": "El movimiento fue regitrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  

@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-all", tags=['parking'])
async def get_all_parking(request:Request, token: TokenData = Depends(verify_token)):
    try:      
        db = Session()  
        parking = db.query(ParkingModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(parking))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()

@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-all-counter", tags=['parking'])
async def get_all_parking_counter(request:Request, token: TokenData = Depends(verify_token)):
    try:
        db = Session()
        parking = db.query(ParkingModel).all()
     
        in_parking_motorcycle = 0
        in_parking_bycicle = 0
        out_of_parking_motorcycle = 0
        out_of_parking_bycicle = 0
        parking_motocycle_capacity = 3
        parking_bycicle_capacity = 20
        percent_motorcycle_not_ocupation = 0
        percent_motorcycle_ocupation = 0
        percent_bycicle_ocupation = 0
        percent_bycicle_not_ocupation = 0     
        
        for doc in parking:
            if doc.vehicle_type == 1 and doc.is_in_parking == 1:
                in_parking_motorcycle += 1
            elif doc.vehicle_type == 1 and doc.is_in_parking == 0:
                out_of_parking_motorcycle += 1
            elif doc.vehicle_type == 2 and doc.is_in_parking == 1:
                in_parking_bycicle += 1
            elif doc.vehicle_type == 2 and doc.is_in_parking == 0:
                out_of_parking_bycicle += 1
                
        
        parking_actually_motorcycle_capacity = parking_motocycle_capacity - in_parking_motorcycle
        parking_actually_bycicle_capacity = parking_bycicle_capacity - in_parking_bycicle
        
        percent_motorcycle_ocupation = (in_parking_motorcycle * 100) / parking_motocycle_capacity
        percent_motorcycle_not_ocupation = 100 - percent_motorcycle_ocupation
        percent_bycicle_ocupation = (in_parking_bycicle * 100) / parking_bycicle_capacity
        percent_bycicle_not_ocupation = 100 - percent_bycicle_ocupation
        
        response = {
            "motocycle_in_parking": in_parking_motorcycle,
            "bycicle_in_parking": in_parking_bycicle,
            "actually_motorcycle_capacity": parking_actually_motorcycle_capacity,
            "actually_bycicle_capacity": parking_actually_bycicle_capacity,
            "capacity_motorcycle": parking_motocycle_capacity,
            "capacity_bycicle": parking_bycicle_capacity,
            "percent_motorcycle_ocupation": percent_motorcycle_ocupation,
            "percent_motorcycle_not_ocupation": percent_motorcycle_not_ocupation,
            "percent_bycicle_ocupation": percent_bycicle_ocupation,
            "percent_bycicle_not_ocupation": percent_bycicle_not_ocupation        
        }
        
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()


@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-by-document/{user_document}", tags=['parking'])
async def get_parking_by_document(request:Request, user_document: int, token: TokenData = Depends(verify_token)):
    try:      
        db = Session()  
        parking = db.query(ParkingModel).filter(ParkingModel.user_document == user_document).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(parking))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  

@limiter.limit("30/minute")
@parking_router.put("/api/v1/parking-registration-update/{user_document}", tags=['parking'])
async def update_parking(request:Request, user_document: int, parking: Parking, token: TokenData = Depends(verify_token)):
    try:
        db = Session()
        parking_record = db.query(ParkingModel).filter(ParkingModel.user_document == user_document).first()

        if not parking_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró un registro de parqueo para este usuario"
            )

        parking_record.is_in_parking = parking.is_in_parking
        parking_record.updated_at = datetime.now()
        db.commit()

        return {"message": "El registro de parqueo fue actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  