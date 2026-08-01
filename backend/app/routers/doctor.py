from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.doctor import Department, Specialization
from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorListResponse,
)
from app.services.doctor_services import DoctorService


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.post("/create", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.create_doctor(
        database=db,
        data=doctor,
        created_by=current_user.id,
    )


@router.get("", response_model=DoctorListResponse)
def get_all_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    department: Optional[str] = Query(None),
    specialization: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.get_all_doctors(
        database=db,
        page=page,
        limit=limit,
        search=search,
        department=department,
        specialization=specialization,
    )


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor_by_id(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.get_doctor_by_id(
        database=db,
        doctor_id=doctor_id,
    )


@router.put("/update/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: str,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.update_doctor(
        database=db,
        doctor_id=doctor_id,
        data=doctor,
    )


@router.delete("/delete/{doctor_id}", response_model=DoctorResponse)
def delete_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.delete_doctor(
        database=db,
        doctor_id=doctor_id,
    )


@router.patch("/restore/{doctor_id}", response_model=DoctorResponse)
def restore_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return DoctorService.restore_doctor(
        database=db,
        doctor_id=doctor_id,
    )