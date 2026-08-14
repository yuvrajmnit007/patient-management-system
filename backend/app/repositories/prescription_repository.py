from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models.prescription import Prescription


class PrescriptionRepository:

    @staticmethod
    def create_prescription(
        database: Session, prescription: Prescription
    ) -> Prescription:
        database.add(prescription)
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def update_prescription(
        database: Session, prescription: Prescription
    ) -> Prescription:
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def get_last_prescription(database: Session) -> Prescription | None:
        return (
            database.query(Prescription)
            .order_by(Prescription.id.desc())
            .first()
        )

    @staticmethod
    def get_prescription_by_id(
        database: Session, prescription_id: str
    ) -> Prescription | None:
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
    def get_any_prescription(
        database: Session, prescription_id: str
    ) -> Prescription | None:
        return (
            database.query(Prescription)
            .filter(Prescription.prescription_id == prescription_id)
            .first()
        )

    @staticmethod
    def get_by_appointment_id(
        database: Session, appointment_pk: int
    ) -> Prescription | None:
        """Look up by the numeric appointment PK (appointment.id), not the string appointment_id."""
        return (
            database.query(Prescription)
            .filter(
                Prescription.appointment_id == appointment_pk,
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
    ) -> tuple[list[Prescription], int]:
        query = (
            database.query(Prescription)
            .options(
                joinedload(Prescription.appointment),
                joinedload(Prescription.prescription_items),
            )
            .filter(Prescription.is_active == True)
        )

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Prescription.prescription_id.ilike(pattern),
                    Prescription.diagnosis.ilike(pattern),
                    Prescription.advice.ilike(pattern),
                )
            )

        total = query.count()
        prescriptions = (
            query.order_by(Prescription.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return prescriptions, total

    @staticmethod
    def delete_prescription(
        database: Session, prescription: Prescription
    ) -> Prescription:
        prescription.is_active = False
        database.commit()
        database.refresh(prescription)
        return prescription

    @staticmethod
    def restore_prescription(
        database: Session, prescription: Prescription
    ) -> Prescription:
        prescription.is_active = True
        database.commit()
        database.refresh(prescription)
        return prescription