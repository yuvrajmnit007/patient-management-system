from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole
    password: str


class UserResponse(BaseModel):
    id:int
    username=str
    email: EmailStr
    phone_number: str
    role: UserRole

    class Config:
        from_attributes = True