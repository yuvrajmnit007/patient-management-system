from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:

    @staticmethod
    def generate_patient_id(database: Session) -> str:
        last = PatientRepository.get_last_patient(database)
        if not last:
            return "HM00000001"
        return f"HM{int(last.patient_id[2:]) + 1:08d}"

    @staticmethod
    def create_patient(
        database: Session, data: PatientCreate, created_by: int
    ) -> Patient:
        if data.email and PatientRepository.get_by_email(database, data.email):
            raise ValueError("Email already exists")
        if PatientRepository.get_by_phone_number(database, data.phone_number):
            raise ValueError("Phone number already exists")

        patient = Patient(
            patient_id=PatientService.generate_patient_id(database),
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            blood_group=data.blood_group,
            phone_number=data.phone_number,
            email=data.email,
            address=data.address,
            emergency_contact_name=data.emergency_contact_name,
            emergency_contact_number=data.emergency_contact_number,
            allergies=data.allergies,
            medical_history=data.medical_history,
            created_by=created_by,
        )
        return PatientRepository.create_patient(database, patient)

    @staticmethod
    def update_patient(
        database: Session, patient_id: str, data: PatientUpdate
    ) -> Patient:
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )

        if data.email and data.email != patient.email:
            existing = PatientRepository.get_by_email(database, data.email)
            if existing and existing.id != patient.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )

        if data.phone_number and data.phone_number != patient.phone_number:
            existing = PatientRepository.get_by_phone_number(database, data.phone_number)
            if existing and existing.id != patient.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already exists",
                )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, key, value)

        return PatientRepository.update_patient(database, patient)

    @staticmethod
    def get_all_patients(
        database: Session, page: int, limit: int, search: str | None = None
    ) -> dict:
        patients, total = PatientRepository.get_all(database, page, limit, search)
        return {
            "items": patients,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit if limit else 0,
        }

    @staticmethod
    def get_active_patient_by_id(database: Session, patient_id: str) -> Patient:
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )
        return patient

    @staticmethod
    def delete_patient(database: Session, patient_id: str) -> Patient:
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )
        return PatientRepository.delete_patient(database, patient)

    @staticmethod
    def restore_patient(database: Session, patient_id: str) -> Patient:
        patient = PatientRepository.get_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )
        if patient.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient is already active",
            )
        return PatientRepository.restore_patient(database, patient)