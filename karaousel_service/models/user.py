import uuid
from pydantic import BaseModel, Field, SecretStr
from pydantic.networks import EmailStr
from typing import Optional
from typing import List

class User(BaseModel):
    id: int
    name: str 
    email: EmailStr = Field(unique=True, index=True)
    date: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "Dolly",
                "email": "dollyna@gmail.com",
                "date": "05-12-2023"
            }
        }
    

        
class UpdateUser(BaseModel):
    email: Optional[str] 
    date: Optional[str]