from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[AppointmentStatus] = None



class AppointmentCreate(AppointmentBase):
    patient_id: str = Field(..., example="PAT00000001")
    doctor_id: str = Field(..., example="DOC00000001")
    appointment_date: date = Field(..., example="2026-08-05")
    appointment_time: time = Field(..., example="10:30:00")
    reason: str = Field(..., example="High Fever")


class AppointmentUpdate(AppointmentBase):
    pass


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
    notes: Optional[str]

    status: AppointmentStatus
    is_active: bool

    created_at: datetime
    updated_at: datetime
    created_by: int


class AppointmentListResponse(BaseModel):
    page: int
    limit: int
    total: int
    appointments: list[AppointmentResponse]