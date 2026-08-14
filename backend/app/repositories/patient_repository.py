from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.patient import Patient


class PatientRepository:

    @staticmethod
    def create_patient(database: Session, patient: Patient) -> Patient:
        database.add(patient)
        database.commit()
        database.refresh(patient)
        return patient

    @staticmethod
    def update_patient(database: Session, patient: Patient) -> Patient:
        database.commit()
        database.refresh(patient)
        return patient

    @staticmethod
    def get_last_patient(database: Session) -> Patient | None:
        return database.query(Patient).order_by(Patient.id.desc()).first()

    @staticmethod
    def get_by_email(database: Session, email: str) -> Patient | None:
        return database.query(Patient).filter(Patient.email == email).first()

    @staticmethod
    def get_by_phone_number(database: Session, phone_number: str) -> Patient | None:
        return (
            database.query(Patient)
            .filter(Patient.phone_number == phone_number)
            .first()
        )

    @staticmethod
    def get_active_patient_by_id(database: Session, patient_id: str) -> Patient | None:
        return (
            database.query(Patient)
            .filter(Patient.patient_id == patient_id, Patient.is_active == True)
            .first()
        )

    @staticmethod
    def get_patient_by_id(database: Session, patient_id: str) -> Patient | None:
        return (
            database.query(Patient)
            .filter(Patient.patient_id == patient_id)
            .first()
        )

    @staticmethod
    def get_all(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> tuple[list[Patient], int]:
        query = database.query(Patient).filter(Patient.is_active == True)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Patient.full_name.ilike(pattern),
                    Patient.patient_id.ilike(pattern),
                    Patient.phone_number.ilike(pattern),
                )
            )

        total = query.count()
        patients = (
            query.order_by(Patient.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return patients, total

    @staticmethod
    def delete_patient(database: Session, patient: Patient) -> Patient:
        patient.is_active = False
        database.commit()
        database.refresh(patient)
        return patient

    @staticmethod
    def restore_patient(database: Session, patient: Patient) -> Patient:
        patient.is_active = True
        database.commit()
        database.refresh(patient)
        return patient