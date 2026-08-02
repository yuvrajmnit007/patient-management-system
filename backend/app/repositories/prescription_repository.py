from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models.prescription import Prescription


class PrescriptionRepository:

    @staticmethod
    def create_prescription(database: Session, prescription: Prescription):
        database.add(prescription)
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def update_prescription(database: Session, prescription: Prescription):
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def get_last_prescription(database: Session):
        return (
            database.query(Prescription)
            .order_by(Prescription.id.desc())
            .first()
        )

    @staticmethod
    def get_prescription_by_id(database: Session, prescription_id: str):
        return (
            database.query(Prescription)
            .options(
                joinedload(Prescription.appointment),
                joinedload(Prescription.prescription_items),
            )
            .filter(
                Prescription.prescription_id == prescription_id,
                Prescription.is_active == True,
            )
            .first()
        )

    @staticmethod
    def get_any_prescription(database: Session, prescription_id: str):
        return (
            database.query(Prescription)
            .filter(
                Prescription.prescription_id == prescription_id
            )
            .first()
        )

    @staticmethod
    def get_by_appointment(database: Session, appointment_id: int):
        return (
            database.query(Prescription)
            .filter(
                Prescription.appointment_id == appointment_id,
                Prescription.is_active == True,
            )
            .first()
        )

    @staticmethod
    def get_all_prescriptions(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
    ):

        query = (
            database.query(Prescription)
            .options(
                joinedload(Prescription.appointment),
                joinedload(Prescription.prescription_items),
            )
            .filter(
                Prescription.is_active == True
            )
        )

        if search:
            query = query.filter(
                or_(
                    Prescription.prescription_id.ilike(f"%{search}%"),
                    Prescription.diagnosis.ilike(f"%{search}%"),
                    Prescription.advice.ilike(f"%{search}%"),
                )
            )

        total = query.count()

        prescriptions = (
            query
            .order_by(Prescription.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return prescriptions, total

    @staticmethod
    def delete_prescription(database: Session, prescription: Prescription):
        prescription.is_active = False
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def restore_prescription(database: Session, prescription: Prescription):
        prescription.is_active = True
        database.commit()
        database.refresh(prescription)
        return prescription