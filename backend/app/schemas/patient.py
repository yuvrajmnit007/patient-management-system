from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.patient import Gender, BloodGroup


def _validate_dob(value: Optional[date]) -> Optional[date]:
    if value is None:
        return value
    if value > date.today():
        raise ValueError("Date of birth cannot be in the future")
    return value


def _validate_phone(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    if not value.isdigit():
        raise ValueError("Phone number must contain only digits")
    if len(value) != 10:
        raise ValueError("Phone number must be exactly 10 digits")
    return value


class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

    _v_dob = field_validator("date_of_birth")(_validate_dob)
    _v_phone = field_validator("phone_number")(_validate_phone)
    _v_ec_phone = field_validator("emergency_contact_number")(_validate_phone)


class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

    _v_dob = field_validator("date_of_birth")(_validate_dob)
    _v_phone = field_validator("phone_number")(_validate_phone)
    _v_ec_phone = field_validator("emergency_contact_number")(_validate_phone)


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: str
    full_name: str
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime