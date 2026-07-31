from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.patient import Patient


class PatientRepository:
    @staticmethod
    def create_patient(database: Session, patient: Patient):
        database.add(patient)
        database.commit()
        database.refresh(patient)
        return patient

    @staticmethod
    def get_by_patient_id(database: Session, patient_id: str):
        return database.query(Patient).filter(Patient.patient_id == patient_id).first()

    @staticmethod
    def get_all(database: Session,page:int ,limit:int,search: str | None = None):
        offset = (page - 1) * limit
        query = database.query(Patient)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Patient.full_name.ilike(search_pattern),
                    Patient.patient_id.ilike(search_pattern),
                    Patient.phone_number.ilike(search_pattern)
                )
            )
            total= query.count()
            patients = query.offset(offset).limit(limit).all()
            return patients, total
        else:
            return query.offset(offset).limit(limit).all(), query.count()

    @staticmethod
    def get_by_id(database: Session, id: int):
        return database.query(Patient).filter(Patient.id == id).first()

    @staticmethod
    def get_by_email(database: Session, email: str):
        return database.query(Patient).filter(Patient.email == email).first()


    @staticmethod
    def get_by_phone_number(database: Session, phone_number: str):
        return database.query(Patient).filter(Patient.phone_number == phone_number).first()


    @staticmethod
    def get_last_patient(database: Session):
        return database.query(Patient).order_by(Patient.id.desc()).first()

    @staticmethod
    def update_patient(database: Session, patient: Patient):
        database.commit()
        database.refresh(patient)
        return patient


    @staticmethod
    def delete_patient(database: Session, patient: Patient):
        patient.is_active = False
        database.commit()
        database.refresh(patient)
        return patient
