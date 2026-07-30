from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientListResponse, PatientResponse, PatientUpdate
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.patient_services import PatientService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/create", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_patient = PatientService.create_patient(db, patient, created_by=current_user.id)
        return new_patient
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put("/update/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: str, patient: PatientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        updated_patient = PatientService.update_patient(db, patient_id, patient)
        return updated_patient
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list", response_model=PatientListResponse)
def get_all_patients(page: int = 1, limit: int = 10, search: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patients_data = PatientService.get_all_patients(db, page, limit, search)
    return patients_data