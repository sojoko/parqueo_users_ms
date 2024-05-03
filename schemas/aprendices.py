from pydantic import BaseModel, Field
from typing import Optional

class Aprendices(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del aprendiz")
    name: str = Field(..., description="Nombre del aprendiz")
    last_name: str = Field(..., description="Apellido del aprendiz")
    document: int = Field(..., description="Documento del aprendiz")
    ficha: int = Field(..., description="Ficha del aprendiz")
    email: str  = Field(..., description="Correo electronico del aprendiz")
    photo: Optional[str] = Field(None, description="La url de la imagen del aprendiz")
    finish_date: str = Field(..., description="Fecha de finalización del aprendizaje")
    state_id: Optional[int] = Field(None, description="Estado del aprendiz")
    

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jonhathan",
                "last_name": "Sojo",
                "document": "123456789",
                "ficha": "123456",
                "photo": "https://example.com/image.jpg",
                 "finish_date": "2021-12-31"
            }
        }


class ChangeStatusRequest(BaseModel):
    document: int
    state_id: int