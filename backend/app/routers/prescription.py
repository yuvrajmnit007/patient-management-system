from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionListResponse,
)

from app.services.prescription_services import PrescriptionService


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"],
)


@router.post("/create", response_model=PrescriptionResponse)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.create_prescription(
        database=db,
        data=prescription,
        created_by=current_user.id,
    )


@router.get("", response_model=PrescriptionListResponse)
def get_all_prescriptions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.get_all_prescriptions(
        database=db,
        page=page,
        limit=limit,
        search=search,
    )


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription_by_id(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.get_prescription_by_id(
        database=db,
        prescription_id=prescription_id,
    )


@router.put("/update/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: str,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.update_prescription(
        database=db,
        prescription_id=prescription_id,
        data=prescription,
    )


@router.delete("/delete/{prescription_id}", response_model=PrescriptionResponse)
def delete_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.delete_prescription(
        database=db,
        prescription_id=prescription_id,
    )


@router.patch("/restore/{prescription_id}", response_model=PrescriptionResponse)
def restore_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PrescriptionService.restore_prescription(
        database=db,
        prescription_id=prescription_id,
    )