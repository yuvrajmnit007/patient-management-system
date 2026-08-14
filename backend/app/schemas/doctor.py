from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.doctor import Department, DoctorStatus, Specialization


class DoctorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: Optional[str] = None
    specialization: Optional[Specialization] = None
    department: Optional[Department] = None
    qualification: Optional[str] = None
    experience: Optional[int] = Field(None, ge=0, le=60)
    consultation_fee: Optional[float] = Field(None, ge=0)
    availability: Optional[str] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    @field_validator("specialization", mode="before")
    @classmethod
    def _v_spec(cls, value):
        if value is None or isinstance(value, Specialization):
            return value
        normalized = value.strip().replace(" ", "_").upper()
        for item in Specialization:
            if item.name == normalized or item.value == value:
                return item
        raise ValueError(
            f"Invalid specialization. Allowed: {[i.value for i in Specialization]}"
        )

    @field_validator("department", mode="before")
    @classmethod
    def _v_dept(cls, value):
        if value is None or isinstance(value, Department):
            return value
        normalized = value.strip().replace(" ", "_").upper()
        for item in Department:
            if item.name == normalized or item.value == value:
                return item
        raise ValueError(
            f"Invalid department. Allowed: {[i.value for i in Department]}"
        )


class DoctorRegister(DoctorBase):
    password: str = Field(..., min_length=8, examples=["securepassword123"])
    full_name: str = Field(..., examples=["Dr. John Doe"])
    department: Department = Field(..., examples=[Department.MEDICINE])
    specialization: Specialization = Field(..., examples=[Specialization.CARDIOLOGY])
    qualification: str = Field(..., examples=["MBBS, MD"])
    experience: int = Field(..., ge=0)
    consultation_fee: float = Field(..., ge=0)
    availability: Optional[str] = Field(None, examples=["Mon-Sat 10:00 AM - 5:00 PM"])
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: EmailStr = Field(..., examples=["doctor@gmail.com"])  # required
    address: Optional[str] = Field(None, examples=["Jaipur"])


class DoctorUpdate(DoctorBase):
    pass


class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: str
    full_name: str
    specialization: Specialization
    department: Department
    qualification: str
    experience: int
    consultation_fee: float
    availability: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    is_active: bool
    status: DoctorStatus
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime