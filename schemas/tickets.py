from pydantic import BaseModel, Field
from typing import Optional

class Tickets(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del ticket")
    user_id: Optional[int] = Field(None, description="id del usuario")
    document: Optional [int] = Field(None, description="Documento del usuario") 
    vehicle_type: Optional [str] = Field(None, description="Tipo de vehiculo")
    placa: Optional [str] = Field(None, description="Placa de la motocicleta")
    numero_marco: Optional [str] = Field(None, description="Placa de la motocicleta")
    date: Optional [str] = Field(None, description="Fecha ingresada por el usuario")
    description: Optional [str] = Field(None, description="Descripcion del ticket")
    photo: Optional[str] = Field(None, description="La url de la imagen del aprendiz")
    status: Optional [int] = Field(None, description="Estado del ticket creado") 
    create_date: Optional[str] = Field(None, description="Fecha de registro del vigilante")
    response_subject: Optional [str] = Field(None, description="Asunto de la respuesta del ticket")
    response_body: Optional [str] = Field(None, description="Cuerpo de la respuesta del ticket")



    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "document": "1683822",
                "vehicle_type": "Motocicleta",
                "placa": "PFM40G",
                "numero_marco": "0",
                "date": "2022-05-06",
                "description": "La moto tiene un rayón en el tanque de combustible",
                "photo": "https://example.com/image.jpg",
                "status": "1"
            }
        }
        
        
