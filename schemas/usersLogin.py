from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = Field(None, description="Identificador unico del usuario")   
    document: int = Field(..., description="Documento del usuario")
    password: str = Field(..., description="Ficha del usuario")
 

    class Config:
        schema_extra = {
            "example": {
                "id": 1,                
                "document": "123456789",
                "password": "123456",
                
                
            }
        }
