from datetime import datetime
from config.database import Session
from fastapi import HTTPException
from models.parking import Parking as ParkingModel

class ParkingRepository:
    def create_parking(self, parking_data: dict):
        db = Session()
        try:
            user_exist = db.query(ParkingModel).filter(ParkingModel.user_document == parking_data["user_document"]).first()
            if user_exist:
                return False
                
            new_parking = ParkingModel(**parking_data)
            db.add(new_parking)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_all_parking(self):
        db = Session()
        try:      
            parking = db.query(ParkingModel).all()
            return parking
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_all_parking_counter(self):
        db = Session()
        try:
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
            
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_parking_by_document(self, user_document: int):
        db = Session()
        try:      
            parking = db.query(ParkingModel).filter(ParkingModel.user_document == user_document).first()
            return parking
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def update_parking(self, user_document: int, parking_data: dict):
        db = Session()
        try:
            parking_record = db.query(ParkingModel).filter(ParkingModel.user_document == user_document).first()

            if not parking_record:
                return False

            for key, value in parking_data.items():
                setattr(parking_record, key, value)
                
            parking_record.updated_at = datetime.now()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()