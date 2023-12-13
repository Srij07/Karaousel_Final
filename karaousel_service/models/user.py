import uuid
from pydantic import BaseModel, Field, SecretStr
from pydantic.networks import EmailStr
from typing import Optional
from typing import List
import strawberry

@strawberry.type
class User:
    id: int
    name: str 
    email: str
    date: str
    password: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "Dolly",
                "email": "dollyna@gmail.com",
                "date": "05-12-2023",
                "password": "asnvhgkl"
            }
        }
    

        
class UpdateUser(BaseModel):
    email: Optional[str] 
    date: Optional[str]
    
class Token(BaseModel):
    access: Optional[str]
    refresh: Optional[str]
    
class TokenRequest(BaseModel):
    email: str
    password: Optional[str]