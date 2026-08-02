from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

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
    def validate_specialization(cls, value):
        if value is None:
            return value

        if isinstance(value, Specialization):
            return value

        value = value.strip().replace(" ", "_").upper()

        for item in Specialization:
            if item.name == value:
                return item

        raise ValueError(
            f"Invalid specialization. Allowed values: {[i.name for i in Specialization]}"
        )

    @field_validator("department", mode="before")
    @classmethod
    def validate_department(cls, value):
        if value is None:
            return value

        if isinstance(value, Department):
            return value

        value = value.strip().replace(" ", "_").upper()

        for item in Department:
            if item.name == value:
                return item

        raise ValueError(
            f"Invalid department. Allowed values: {[i.name for i in Department]}"
        )

class DoctorRegister(DoctorBase):
    password: str = Field(..., min_length=8, example="securepassword123")
    full_name: str = Field(..., example="Dr. John Doe")
    department: Department = Field(..., example=Department.MEDICINE)
    specialization: Specialization = Field(..., example=Specialization.CARDIOLOGY)
    qualification: str = Field(..., example="MBBS, MD")
    experience: int = Field(..., ge=0, example=8)
    consultation_fee: float = Field(..., ge=0, example=700)
    availability: Optional[str] = Field(None, example="Mon-Sat 10:00 AM - 5:00 PM")
    phone_number: str = Field(..., min_length=10, max_length=15, example="+919876543210")
    email: Optional[EmailStr] = Field(None, example="doctor@gmail.com")
    address: Optional[str] = Field(None, example="Jaipur")






class DoctorCreate(DoctorBase):
    full_name: str = Field(..., example="Dr. John Doe")
    specialization: Specialization = Field(..., example=Specialization.CARDIOLOGY)
    department: Department = Field(..., example=Department.MEDICINE)
    qualification: str = Field(..., example="MBBS, MD")
    experience: int = Field(..., ge=0, example=8)
    consultation_fee: float = Field(..., ge=0, example=700)
    availability: Optional[str] = Field(
        None,
        example="Mon-Sat 10:00 AM - 5:00 PM"
    )
    phone_number: str = Field(..., example="+919876543210")
    email: Optional[EmailStr] = Field(
        None,
        example="doctor@gmail.com"
    )
    address: Optional[str] = Field(
        None,
        example="Jaipur"
    )


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
    availability: Optional[str]
    phone_number: str
    email: Optional[EmailStr]
    address: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    status: DoctorStatus


class DoctorListResponse(BaseModel):
    page: int
    limit: int
    total: int
    doctors: list[DoctorResponse]