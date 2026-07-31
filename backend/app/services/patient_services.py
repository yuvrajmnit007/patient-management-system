from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from fastapi import HTTPException, status



class PatientService:
    
    @staticmethod
    def create_patient(database: Session, data: PatientCreate,created_by: int):
        existing_email = PatientRepository.get_by_email(database, data.email)
        existing_phone = PatientRepository.get_by_phone_number(database, data.phone_number)


        if existing_email:
            raise ValueError("Email already exists")

        if existing_phone:
            raise ValueError("Phone number already exists")

        patient_id = PatientService.generate_patient_id(database)
        patient = Patient(
            patient_id=patient_id,
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
            created_by=created_by
        )

        return PatientRepository.create_patient(database, patient)

    @staticmethod
    def generate_patient_id(database: Session):
        last_patient = PatientRepository.get_last_patient(database)
        if last_patient:
            last_id = int(last_patient.patient_id[2:])
            new_id = f"HM{last_id + 1:08d}"
        else:
            new_id = "HM00000001"
        return new_id


    @staticmethod
    def update_patient(database: Session, patient_id: str, data: PatientUpdate):
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        print("Patient to update:", patient_id)
        if not patient:
            raise ValueError("Patient not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(patient, field, value)

        return PatientRepository.update_patient(database, patient)

    @staticmethod
    def get_all_patients(database: Session, page: int, limit: int, search: str | None = None):
        patients, total = PatientRepository.get_all(database, page, limit, search)
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": patients
        }

    @staticmethod
    def delete_patient(database: Session, patient_id: str):
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        if not patient.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient is already deleted")
        return PatientRepository.delete_patient(database, patient)

    @staticmethod
    def get_active_patient_by_id(database: Session, patient_id: str):
        patient = PatientRepository.get_active_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    @staticmethod
    def get_patient_by_id(database: Session, patient_id: str):
        patient = PatientRepository.get_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    @staticmethod
    def restore_patient(database: Session, patient_id: str):
        patient = PatientRepository.get_patient_by_id(database, patient_id)
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        if patient.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient is already active")
        patient.is_active = True
        return PatientRepository.update_patient(database, patient)