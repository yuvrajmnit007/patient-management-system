from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.user import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    role: UserRole
    password: str = Field(..., min_length=8)

    @field_validator("role")
    @classmethod
    def restrict_role(cls, value: UserRole) -> UserRole:
        # /auth/register is for admin/receptionist accounts only.
        # Doctors register via /doctors/register (creates User + Doctor together).
        if value == UserRole.DOCTOR:
            raise ValueError("Doctors must register via /doctors/register")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str