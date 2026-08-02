from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field



class PrescriptionItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None


class PrescriptionItemCreate(PrescriptionItemBase):
    medicine_name: str = Field(..., example="Paracetamol")
    dosage: str = Field(..., example="500 mg")
    frequency: str = Field(..., example="Twice Daily")
    duration: str = Field(..., example="5 Days")


class PrescriptionItemUpdate(PrescriptionItemBase):
    pass


class PrescriptionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicine_name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str]



class PrescriptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: Optional[str] = None
    diagnosis: Optional[str] = None
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None


class PrescriptionCreate(PrescriptionBase):
    appointment_id: str = Field(..., example="APT00000001")
    diagnosis: str = Field(..., example="Viral Fever")
    advice: Optional[str] = Field(
        None,
        example="Drink plenty of water"
    )
    follow_up_date: Optional[date] = Field(
        None,
        example="2026-08-10"
    )

    medicines: list[PrescriptionItemCreate]


class PrescriptionUpdate(PrescriptionBase):
    medicines: Optional[list[PrescriptionItemUpdate]] = None


class PrescriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prescription_id: str

    appointment_id: str

    diagnosis: str
    advice: Optional[str]
    follow_up_date: Optional[date]

    medicines: list[PrescriptionItemResponse]

    is_active: bool

    created_by: int

    created_at: datetime
    updated_at: datetime


class PrescriptionListResponse(BaseModel):
    page: int
    limit: int
    total: int

    prescriptions: list[PrescriptionResponse]