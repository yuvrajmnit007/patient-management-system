from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole
    password: str


class UserResponse(BaseModel):
    id:int
    username:str
    full_name:str
    email: EmailStr
    phone_number: str
    role: UserRole

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str