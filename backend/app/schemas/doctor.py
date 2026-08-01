from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.doctor import Department, Specialization


class DoctorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: Optional[str] = None
    specialization: Optional[Specialization] = None
    department: Optional[Department] = None
    phone_number: Optional[str] = None
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


class DoctorCreate(DoctorBase):
    full_name: str = Field(..., example="Dr. John Doe")
    specialization: Specialization = Field(..., example=Specialization.CARDIOLOGY)
    department: Department = Field(..., example=Department.MEDICINE)
    phone_number: str = Field(..., example="+919876543210")
    email: Optional[EmailStr] = Field(None, example="doctor@gmail.com")
    address: Optional[str] = Field(None, example="Jaipur")


class DoctorUpdate(DoctorBase):
    pass


class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: str
    full_name: str
    specialization: Specialization
    department: Department
    phone_number: str
    email: Optional[EmailStr]
    address: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str
    created_by: Optional[int]


class DoctorListResponse(BaseModel):
    page: int
    limit: int
    total: int
    doctors: list[DoctorResponse]