from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.appointment import AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentListResponse,
)
from app.services.appointment_services import AppointmentService


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/create", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.create_appointment(
        database=db,
        data=appointment,
        created_by=current_user.id,
    )


@router.get("", response_model=AppointmentListResponse)
def get_all_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    doctor_id: Optional[str] = Query(None),
    patient_id: Optional[str] = Query(None),
    appointment_status: Optional[AppointmentStatus] = Query(None),
    appointment_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.get_all_appointments(
        database=db,
        page=page,
        limit=limit,
        search=search,
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_status=appointment_status,
        appointment_date=appointment_date,
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.get_appointment_by_id(
        database=db,
        appointment_id=appointment_id,
    )


@router.put("/update/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: str,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.update_appointment(
        database=db,
        appointment_id=appointment_id,
        data=appointment,
    )


@router.delete("/delete/{appointment_id}", response_model=AppointmentResponse)
def delete_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.delete_appointment(
        database=db,
        appointment_id=appointment_id,
    )


@router.patch("/restore/{appointment_id}", response_model=AppointmentResponse)
def restore_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.restore_appointment(
        database=db,
        appointment_id=appointment_id,
    )

@router.patch("/confirm/{appointment_id}", response_model=AppointmentResponse)
def confirm_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AppointmentService.confirm_appointment(
        database=db,
        appointment_id=appointment_id,
        current_user_id=current_user.id,
    )