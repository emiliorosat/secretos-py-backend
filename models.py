from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID



# Schemas

class User (BaseModel):
    UserName: str
    Email: Optional[str] = None
    FullName: Optional[str] = None
    Disabled: Optional[bool] = None


class UserAccess (User):
    Password: str
    OldPassword: Optional[str] = None
    
class UserIdentity (User):
    Id: UUID


class Secret (BaseModel):
    Id: Optional[str] = None
    UserId: Optional[str] = None
    Titulo: str
    Description: str
    Value: float
    Date: date
    Place: str
    Lat: float
    Lng: float

class Token(BaseModel):
    access_token: str
    token_type: str

