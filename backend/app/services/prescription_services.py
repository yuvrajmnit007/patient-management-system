from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.appointment import AppointmentStatus
from app.models.prescription import Prescription
from app.models.prescription_item import PrescriptionItem
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.prescription_repository import PrescriptionRepository
from app.repositories.prescription_item_repository import PrescriptionItemRepository
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate


class PrescriptionService:

    @staticmethod
    def generate_prescription_id(database: Session) -> str:
        last = PrescriptionRepository.get_last_prescription(database)
        if not last:
            return "PRS00000001"
        return f"PRS{int(last.prescription_id[3:]) + 1:08d}"

    @staticmethod
    def serialize_prescription(prescription: Prescription) -> dict:
        return {
            "prescription_id": prescription.prescription_id,
            "appointment_id": prescription.appointment.appointment_id,
            "diagnosis": prescription.diagnosis,
            "advice": prescription.advice,
            "follow_up_date": prescription.follow_up_date,
            "medicines": [
                {
                    "medicine_name": item.medicine_name,
                    "dosage": item.dosage,
                    "frequency": item.frequency,
                    "duration": item.duration,
                    "instructions": item.instructions,
                }
                for item in prescription.prescription_items  # <-- FIX
            ],
            "is_active": prescription.is_active,
            "created_by": prescription.created_by,
            "created_at": prescription.created_at,
            "updated_at": prescription.updated_at,
        }

    @staticmethod
    def create_prescription(
        database: Session, data: PrescriptionCreate, created_by: int
    ) -> dict:
        appointment = AppointmentRepository.get_appointment_by_id(
            database, data.appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if appointment.status != AppointmentStatus.CONFIRMED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot create prescription — appointment status is "
                    f"'{appointment.status.value}'; must be 'Confirmed'"
                ),
            )

        # FIX: use integer PK, correct method name
        if PrescriptionRepository.get_by_appointment_id(database, appointment.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prescription for this appointment already exists",
            )

        prescription = Prescription(
            prescription_id=PrescriptionService.generate_prescription_id(database),
            appointment_id=appointment.id,
            diagnosis=data.diagnosis,
            advice=data.advice,
            follow_up_date=data.follow_up_date,
            is_active=True,
            created_by=created_by,
        )
        prescription = PrescriptionRepository.create_prescription(database, prescription)

        # FIX: batch insert using correct repo method
        items = [
            PrescriptionItem(
                prescription_id=prescription.id,
                medicine_name=m.medicine_name,
                dosage=m.dosage,
                frequency=m.frequency,
                duration=m.duration,
                instructions=m.instructions,
            )
            for m in data.medicines
        ]
        PrescriptionItemRepository.create_items(database, items)

        appointment.status = AppointmentStatus.COMPLETED
        database.commit()

        # Re-fetch to eager-load prescription_items + appointment
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription.prescription_id
        )
        return PrescriptionService.serialize_prescription(prescription)

    @staticmethod
    def get_all_prescriptions(
        database: Session, page: int, limit: int, search: str | None = None
    ) -> dict:
        prescriptions, total = PrescriptionRepository.get_all_prescriptions(
            database, page, limit, search
        )
        return {
            "items": [
                PrescriptionService.serialize_prescription(p) for p in prescriptions
            ],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit if limit else 0,
        }

    @staticmethod
    def get_prescription_by_id(database: Session, prescription_id: str) -> dict:
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription_id
        )
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found"
            )
        return PrescriptionService.serialize_prescription(prescription)

    @staticmethod
    def update_prescription(
        database: Session, prescription_id: str, data: PrescriptionUpdate
    ) -> dict:
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription_id
        )
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found"
            )

        update_data = data.model_dump(exclude_unset=True)
        medicines_data = update_data.pop("medicines", None)

        for key, value in update_data.items():
            setattr(prescription, key, value)
        PrescriptionRepository.update_prescription(database, prescription)

        if medicines_data is not None:
            items = [
                PrescriptionItem(
                    prescription_id=prescription.id,
                    medicine_name=m["medicine_name"],
                    dosage=m["dosage"],
                    frequency=m["frequency"],
                    duration=m["duration"],
                    instructions=m.get("instructions"),
                )
                for m in medicines_data
            ]
            PrescriptionItemRepository.replace_items(
                database, prescription.id, items
            )

        # FIX: pass string prescription_id, not int
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription.prescription_id
        )
        return PrescriptionService.serialize_prescription(prescription)

    @staticmethod
    def delete_prescription(database: Session, prescription_id: str) -> dict:
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription_id
        )
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found"
            )
        PrescriptionRepository.delete_prescription(database, prescription)
        return PrescriptionService.serialize_prescription(prescription)

    @staticmethod
    def restore_prescription(database: Session, prescription_id: str) -> dict:
        prescription = PrescriptionRepository.get_any_prescription(
            database, prescription_id
        )
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found"
            )
        if prescription.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prescription is already active",
            )
        PrescriptionRepository.restore_prescription(database, prescription)
        prescription = PrescriptionRepository.get_prescription_by_id(
            database, prescription_id
        )
        return PrescriptionService.serialize_prescription(prescription)