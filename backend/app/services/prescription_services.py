from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.appointment import AppointmentStatus
from app.models.prescription import Prescription
from app.models.prescription_item import PrescriptionItem
from app.repositories.prescription_repository import PrescriptionRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.prescription_item_repository import PrescriptionItemRepository
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate


class PrescriptionService:
    
    @staticmethod
    def generate_prescription_id(database: Session):

        last_prescription = PrescriptionRepository.get_last_prescription(database)

        if not last_prescription:
            return "PRS00000001"

        last_number = int(last_prescription.prescription_id[3:])
        return f"PRS{last_number + 1:08d}"


    @staticmethod
    def serialize_prescription(prescription: Prescription):
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
                    "instructions": item.instructions
                }
                for item in prescription.items
            ],
            "is_active": prescription.is_active,
            "created_by": prescription.created_by,
            "created_at": prescription.created_at,
            "updated_at": prescription.updated_at,
        }


    @staticmethod
    def create_prescription(database: Session, data: PrescriptionCreate, created_by: int):
        appointment = AppointmentRepository.get_appointment_by_id(database, data.appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

        if appointment.status == AppointmentStatus.CANCELLED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create prescription for a cancelled appointment")

        if appointment.status == AppointmentStatus.NO_SHOW:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create prescription for a no-show appointment")

        if appointment.status != AppointmentStatus.CONFIRMED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create prescription for an appointment that is not confirmed")
        
        existing = PrescriptionRepository.get_prescription_by_appointment_id(database, data.appointment_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prescription for this appointment already exists")

        prescription_id = PrescriptionService.generate_prescription_id(database)
        prescription = Prescription(
            prescription_id=prescription_id,
            appointment_id=appointment.id,
            diagnosis=data.diagnosis,
            advice=data.advice,
            follow_up_date=data.follow_up_date,
            is_active=True,
            created_by=created_by
        )

        created_prescription = PrescriptionRepository.create_prescription(database, prescription)

        for item_data in data.medicines:
            item = PrescriptionItem(
                prescription_id=created_prescription.id,
                medicine_name=item_data.medicine_name,
                dosage=item_data.dosage,
                frequency=item_data.frequency,
                duration=item_data.duration,
                instructions=item_data.instructions
            )
            PrescriptionItemRepository.create_prescription_item(database, item)

        appointment.status = AppointmentStatus.COMPLETED
        database.commit()
        database.refresh(appointment)
        return PrescriptionService.serialize_prescription(created_prescription)


    @staticmethod
    def get_all_prescriptions(database: Session, page: int, limit: int, search: str | None = None):
        prescriptions, total = PrescriptionRepository.get_all_prescriptions(database, page, limit, search)
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": [PrescriptionService.serialize_prescription(p) for p in prescriptions]
        }


    @staticmethod
    def get_prescription_by_id(database: Session, prescription_id: str):
        prescription = PrescriptionRepository.get_prescription_by_id(database, prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
        return PrescriptionService.serialize_prescription(prescription)

    @staticmethod
    def update_prescription(database: Session, prescription_id: str, data: PrescriptionUpdate):
        prescription = PrescriptionRepository.get_prescription_by_id(database, prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(prescription, key, value)

        PrescriptionRepository.update_prescription(database, prescription)
        if data.medicines is not None:
            items = []
            for item in data.medicines:
                items.append(
                    PrescriptionItem(
                        prescription_id=prescription.id,
                        medicine_name=item.medicine_name,
                        dosage=item.dosage,
                    frequency=item.frequency,
                    duration=item.duration,
                    instructions=item.instructions
                )
            )
        PrescriptionItemRepository.update_items(database, prescription.id, items)
        prescription=PrescriptionRepository.get_prescription_by_id(database, prescription.id)
        return PrescriptionService.serialize_prescription(prescription)


    @staticmethod
    def delete_prescription(database: Session, prescription_id: str):
        prescription = PrescriptionRepository.get_prescription_by_id(database, prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")

        PrescriptionRepository.delete_prescription(database, prescription)
        return PrescriptionService.serialize_prescription(prescription)


    @staticmethod
    def restore_prescription(database: Session, prescription_id: str):
        prescription = PrescriptionRepository.get_any_prescription(database, prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
        if prescription.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prescription is already active")

        PrescriptionRepository.restore_prescription(database, prescription)
        prescription = PrescriptionRepository.get_prescription_by_id(database, prescription_id)
        return PrescriptionService.serialize_prescription(prescription)