from pydantic import BaseModel, Field
from typing import Optional

class Admins(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del admin")
    name: str = Field(..., description="Nombre del admin")
    last_name: str = Field(..., description="Apellido del Admin")
    document: int = Field(..., description="Documento del Admin")
    registry_date: Optional[str] = Field(None, description="Fecha de registro del Admin")	
 


    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jonhathan",
                "last_name": "Sojo",
                "document": "123456789",                
                
            }
        }
