from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user, require_admin, require_doctor
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.prescription import (
    PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse,
)
from app.services.prescription_services import PrescriptionService


router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("", response_model=PrescriptionResponse, status_code=201)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor),
):
    return PrescriptionService.create_prescription(
        database=db, data=prescription, created_by=current_user.id
    )


@router.get("", response_model=PaginatedResponse[PrescriptionResponse])
def list_prescriptions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PrescriptionService.get_all_prescriptions(db, page, limit, search)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PrescriptionService.get_prescription_by_id(db, prescription_id)


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: str,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor),
):
    return PrescriptionService.update_prescription(
        db, prescription_id, prescription
    )


@router.delete("/{prescription_id}", response_model=PrescriptionResponse)
def delete_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return PrescriptionService.delete_prescription(db, prescription_id)


@router.patch("/{prescription_id}/restore", response_model=PrescriptionResponse)
def restore_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return PrescriptionService.restore_prescription(db, prescription_id)