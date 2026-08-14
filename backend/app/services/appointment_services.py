from datetime import date, datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.appointment import Appointment, AppointmentStatus
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:

    @staticmethod
    def serialize_appointment(appointment: Appointment) -> dict:
        return {
            "appointment_id": appointment.appointment_id,
            "patient_id": appointment.patient.patient_id,
            "patient_name": appointment.patient.full_name,
            "doctor_id": appointment.doctor.doctor_id,
            "doctor_name": appointment.doctor.full_name,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "reason": appointment.reason,
            "notes": appointment.notes,
            "status": appointment.status,
            "is_active": appointment.is_active,
            "created_by": appointment.created_by,
            "created_at": appointment.created_at,
            "updated_at": appointment.updated_at,
        }

    @staticmethod
    def generate_appointment_id(database: Session) -> str:
        last = AppointmentRepository.get_last_appointment(database)
        if not last:
            return "APT00000001"
        return f"APT{int(last.appointment_id[3:]) + 1:08d}"

    @staticmethod
    def create_appointment(
        database: Session, data: AppointmentCreate, created_by: int
    ) -> dict:
        patient = PatientRepository.get_active_patient_by_id(database, data.patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
            )

        doctor = DoctorRepository.get_doctor_by_id(database, data.doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )

        if data.appointment_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment date cannot be in the past",
            )
        if (
            data.appointment_date == date.today()
            and data.appointment_time < datetime.now().time()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment time cannot be in the past",
            )

        if AppointmentRepository.get_doctor_slot(
            database, doctor.id, data.appointment_date, data.appointment_time
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor already has an appointment at this time",
            )

        appointment = Appointment(
            appointment_id=AppointmentService.generate_appointment_id(database),
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=data.appointment_date,
            appointment_time=data.appointment_time,
            reason=data.reason,
            notes=data.notes,
            created_by=created_by,
        )
        appointment = AppointmentRepository.create_appointment(database, appointment)
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment.appointment_id
        )
        return AppointmentService.serialize_appointment(appointment)

    @staticmethod
    def get_all_appointments(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
        doctor_id: str | None = None,
        patient_id: str | None = None,
        appointment_status: AppointmentStatus | None = None,
        appointment_date: date | None = None,
    ) -> dict:
        doctor_pk = None
        if doctor_id:
            d = DoctorRepository.get_doctor_by_id(database, doctor_id)
            if not d:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
                )
            doctor_pk = d.id

        patient_pk = None
        if patient_id:
            p = PatientRepository.get_active_patient_by_id(database, patient_id)
            if not p:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
                )
            patient_pk = p.id

        appointments, total = AppointmentRepository.get_all_appointments(
            database=database, page=page, limit=limit,
            search=search,
            doctor_id=doctor_pk,
            patient_id=patient_pk,
            status=appointment_status,  # <-- FIX: correct kwarg
            appointment_date=appointment_date,
        )
        return {
            "items": [
                AppointmentService.serialize_appointment(a) for a in appointments
            ],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit if limit else 0,
        }

    @staticmethod
    def get_appointment_by_id(database: Session, appointment_id: str) -> dict:
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )
        return AppointmentService.serialize_appointment(appointment)

    @staticmethod
    def update_appointment(
        database: Session, appointment_id: str, data: AppointmentUpdate
    ) -> dict:
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        update_data = data.model_dump(exclude_unset=True)

        if "appointment_date" in update_data or "appointment_time" in update_data:
            new_date = update_data.get(
                "appointment_date", appointment.appointment_date
            )
            new_time = update_data.get(
                "appointment_time", appointment.appointment_time
            )
            slot = AppointmentRepository.get_doctor_slot(
                database, appointment.doctor_id, new_date, new_time
            )
            if slot and slot.id != appointment.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Doctor already has an appointment at this time",
                )

        for key, value in update_data.items():
            setattr(appointment, key, value)

        appointment = AppointmentRepository.update_appointment(database, appointment)
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment.appointment_id
        )
        return AppointmentService.serialize_appointment(appointment)

    @staticmethod
    def delete_appointment(database: Session, appointment_id: str) -> dict:
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )
        appointment = AppointmentRepository.delete_appointment(database, appointment)
        return AppointmentService.serialize_appointment(appointment)

    @staticmethod
    def restore_appointment(database: Session, appointment_id: str) -> dict:
        appointment = AppointmentRepository.get_any_appointment(
            database, appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )
        if appointment.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment is already active",
            )
        appointment = AppointmentRepository.restore_appointment(database, appointment)
        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment.appointment_id
        )
        return AppointmentService.serialize_appointment(appointment)

    @staticmethod
    def confirm_appointment(
        database: Session, appointment_id: str, current_user_id: int
    ) -> dict:
        doctor = DoctorRepository.get_by_user_id(database, current_user_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Only an active doctor account can confirm appointments",
            )

        appointment = AppointmentRepository.get_appointment_by_id(
            database, appointment_id
        )
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if appointment.doctor_id != doctor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to confirm this appointment",
            )

        if appointment.status == AppointmentStatus.CONFIRMED:
            raise HTTPException(400, detail="Appointment is already confirmed")
        if appointment.status == AppointmentStatus.COMPLETED:
            raise HTTPException(400, detail="Cannot confirm a completed appointment")
        if appointment.status == AppointmentStatus.CANCELLED:
            raise HTTPException(400, detail="Cannot confirm a cancelled appointment")

        appointment.status = AppointmentStatus.CONFIRMED
        database.commit()
        database.refresh(appointment)
        return AppointmentService.serialize_appointment(appointment)