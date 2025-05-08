from pydantic import BaseModel, Field
from typing import Optional

class Vigilantes(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del vigilante")
    name: str = Field(..., description="Nombre del vigilante")
    last_name: str = Field(..., description="Apellido del vigilante")
    document: int = Field(..., description="Documento del vigilante") 
    registry_date: Optional[str] = Field(None, description="Fecha de registro del vigilante")
    status: Optional[int] = Field(None, description="Estado del vigilante")



    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jonhathan",
                "last_name": "Sojo",
                "document": "123456789",
                "email": "admin@parqueo,com",

            }
        }


class ChangeStatusRequest(BaseModel):
    id: int
    status_id: int
