from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str = Field(..., examples=["HM00000001"])
    doctor_id: str = Field(..., examples=["DOC00000001"])
    appointment_date: date = Field(..., examples=["2026-08-20"])
    appointment_time: time = Field(..., examples=["10:30:00"])
    reason: str = Field(..., min_length=1)
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    """
    Reschedule / update notes / change status only.
    Changing patient or doctor is intentionally not supported here —
    delete + create a new appointment for those cases.
    """
    model_config = ConfigDict(from_attributes=True)

    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[AppointmentStatus] = None


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: str

    patient_id: str
    patient_name: str

    doctor_id: str
    doctor_name: str

    appointment_date: date
    appointment_time: time

    reason: str
    notes: Optional[str] = None

    status: AppointmentStatus
    is_active: bool

    created_at: datetime
    updated_at: datetime
    created_by: int