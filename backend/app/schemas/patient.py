from datetime import date ,datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict,field_validator
from app.models.patient import Gender , BloodGroup




class PatientCreate(BaseModel):
    full_name:str
    date_of_birth:date
    gender:Gender
    blood_group:Optional[BloodGroup]=None
    phone_number:str
    email:Optional[EmailStr]=None
    address:Optional[str]=None
    emergency_contact_name:Optional[str]=None
    emergency_contact_number:Optional[str]=None
    allergies:Optional[str]=None
    medical_history:Optional[str]=None
    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value


    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10 :
            raise ValueError("Phone number must be of 10 digits")
        return value

class PatientResponse(BaseModel):
    id:int
    patient_id:str
    full_name:str
    date_of_birth:date
    gender:Gender
    blood_group:Optional[BloodGroup]=None
    phone_number:str
    email:Optional[EmailStr]=None
    address:Optional[str]=None
    emergency_contact_name:Optional[str]=None
    emergency_contact_number:Optional[str]=None
    allergies:Optional[str]=None
    medical_history:Optional[str]=None
    is_active:bool
    created_by:int
    created_at:datetime
    updated_at:datetime


    model_config = ConfigDict(from_attributes=True)


class PatientUpdate(BaseModel):
    full_name:Optional[str]=None
    date_of_birth:Optional[date]=None
    gender:Optional[Gender]=None
    blood_group:Optional[BloodGroup]=None
    phone_number:Optional[str]=None
    email:Optional[EmailStr]=None
    address:Optional[str]=None
    emergency_contact_name:Optional[str]=None
    emergency_contact_number:Optional[str]=None
    allergies:Optional[str]=None
    medical_history:Optional[str]=None

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10 :
            raise ValueError("Phone number must be of 10 digits")
        return value

class PatientListResponse(BaseModel):
    total:int
    page:int
    limit:int
    data:list[PatientResponse]
    model_config = ConfigDict(from_attributes=True)
