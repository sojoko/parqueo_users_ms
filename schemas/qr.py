from pydantic import BaseModel, Field
from typing import Optional

class QR(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del usuario")   
    user_document: int = Field(..., description="llave foraena del usuario")
    qr: Optional[bytes] = Field(None, description="qr del usuario")
    registry_date: Optional[str] = Field(None, description="Fecha de creacion del codigo qr")
 

    class Config:
        schema_extra = {
            "example": {
                "id": 1,                
                "user_document": "123456789",
                "qr": "binario del codigo qr",
                "registry_date": "2021-12-31"              
                
            }
        }
