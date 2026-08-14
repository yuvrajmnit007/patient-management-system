from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user, require_admin, require_doctor
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.doctor import DoctorRegister, DoctorUpdate, DoctorResponse
from app.services.doctor_services import DoctorService


router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/register", response_model=DoctorResponse, status_code=201)
def register_doctor(doctor: DoctorRegister, db: Session = Depends(get_db)):
    return DoctorService.register_doctor(db, doctor)


@router.get("", response_model=PaginatedResponse[DoctorResponse])
def list_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    department: Optional[str] = Query(None),
    specialization: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DoctorService.get_all_doctors(
        database=db, page=page, limit=limit,
        search=search, department=department, specialization=specialization,
    )


@router.get("/pending", response_model=List[DoctorResponse])
def list_pending_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.get_pending_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DoctorService.get_doctor_by_id(db, doctor_id)


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: str,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.update_doctor(db, doctor_id, doctor)


@router.delete("/{doctor_id}", response_model=DoctorResponse)
def delete_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.delete_doctor(db, doctor_id)


@router.patch("/{doctor_id}/restore", response_model=DoctorResponse)
def restore_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.restore_doctor(db, doctor_id)


@router.patch("/{doctor_id}/approve", response_model=DoctorResponse)
def approve_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.approve_doctor(db, doctor_id, current_user.id)


@router.patch("/{doctor_id}/reject", response_model=DoctorResponse)
def reject_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return DoctorService.reject_doctor(db, doctor_id)

@router.get("/me", response_model=DoctorResponse)
def get_current_doctor(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor),
):
    return DoctorService.get_current_doctor(db, current_user.id)