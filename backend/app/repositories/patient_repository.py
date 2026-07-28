from sqlalchemy.orm import Session
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
    def get_all(database: Session):
        return database.query(Patient).all()

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