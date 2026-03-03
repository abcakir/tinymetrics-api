from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Basis-Klasse (gemeinsame Felder)
class UserBase(BaseModel):
    email: EmailStr

# Für die Registrierung
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)