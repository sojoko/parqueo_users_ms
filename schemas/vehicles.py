from pydantic import BaseModel, Field
from typing import Optional

class Motocicletas(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico de la motocicleta")
    vehicle_type: Optional[int] = Field(None, description="Tipo de vehiculo")
    user_document: int = Field(..., description="Documento del aprendiz asociado al vehiculo")
    placa: str = Field(..., description="Placa de la motocicleta")
    marca: str = Field(..., description="Marca de la motocicleta")
    modelo: str = Field(..., description="Modelo de la motocicleta")
    color: str = Field(..., description="Color de la motocicleta")
    foto: str = Field(..., description="Foto de la motocicleta")
    tarjeta_propiedad: str = Field(..., description="tarjeta de propiedad de la motocicleta")
    observaciones: str = Field(..., description="observaciones de la motocicleta")
    registry_date: Optional[str] = Field(None, description="Fecha de registro de la motocicleta")
    
   

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_document": "123456789",
                "placa": "ABC123",
                "marca": "Yamaha",
                "color": "Azul",
                "foto": "https://example.com/image.jpg",               
                "tarjeta_propiedad": "https://example.com/image.jpg",
                "observaciones": "observaciones",
                "registry_date": "2021-12-31"              
            }
        }
        
        
class Bicicleta(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico de la motocicleta")
    vehicle_type: Optional[int] = Field(None, description="Tipo de vehiculo")
    user_document: int = Field(..., description="Documento del aprendiz asociado al vehiculo")
    numero_marco: str = Field(..., description="Placa de la motocicleta")
    marca: str = Field(..., description="Marca de la motocicleta")
    modelo: str = Field(..., description="Modelo de la motocicleta")
    color: str = Field(..., description="Color de la motocicleta")
    foto: str = Field(..., description="Foto de la motocicleta")  
    tarjeta_propiedad: str = Field(..., description="tarjeta de propiedad de la motocicleta")
    observaciones: str = Field(..., description="observaciones de la motocicleta")
    registry_date: str = Field(..., description="Fecha de registro de la motocicleta")  
   
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_document": "123456789",
                "placa": "ABC123",
                "marca": "Yamaha",
                "color": "Azul",
                "foto": "https://example.com/image.jpg",
                "soat": "https://example.com/image.jpg",
                "tarjeta_propiedad": "https://example.com/image.jpg",
                "observaciones": "observaciones",
                "registry_date": "2021-12-31"              
            }
        }