from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PrescriptionItemCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicine_name: str = Field(..., examples=["Paracetamol"])
    dosage: str = Field(..., examples=["500 mg"])
    frequency: str = Field(..., examples=["Twice Daily"])
    duration: str = Field(..., examples=["5 Days"])
    instructions: Optional[str] = None


class PrescriptionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicine_name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None


class PrescriptionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: str = Field(..., examples=["APT00000001"])
    diagnosis: str = Field(..., min_length=1)
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None
    medicines: list[PrescriptionItemCreate] = Field(..., min_length=1)


class PrescriptionUpdate(BaseModel):
    """
    Update diagnosis/advice/follow-up. If `medicines` is provided,
    the entire item list is replaced with the new set (all fields required).
    """
    model_config = ConfigDict(from_attributes=True)

    diagnosis: Optional[str] = None
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None
    medicines: Optional[list[PrescriptionItemCreate]] = None


class PrescriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prescription_id: str
    appointment_id: str
    diagnosis: str
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None
    medicines: list[PrescriptionItemResponse]
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime