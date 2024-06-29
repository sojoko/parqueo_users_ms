from pydantic import BaseModel, Field
from typing import Optional

class Parking(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del usuario")   
    user_document: int = Field(..., description="llave foraena del usuario")
    is_in_parking: int = Field(..., description="Estado del usuario en el parqueadero")
    vehicle_type: Optional[int] = Field(None, description="Tipo de vehiculo")
    created_at: Optional[str] = Field(None, description="Fecha de creacion del registro")
    updated_at: Optional[str] = Field(None, description="Fecha de actualizacion del registro")
    deleted_at: Optional[str] = Field(None, description="Fecha de borrado logico del usuario")
 

    class Config:
        schema_extra = {
            "example": {
                "id": 1,                
                "user_document": "123456789",
                "vehicle_type:": "1",
                "is_in_parking": "1",
                "created_at": "2021-12-31",  
                "updated_at": "2021-12-31",  
                "deleted_at": "2021-12-31",                              
            }
        }
