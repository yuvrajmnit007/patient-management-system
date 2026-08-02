from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.appointment import Appointment, AppointmentStatus
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:

    @staticmethod
    def serialize_appointment(appointment: Appointment):

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
    def generate_appointment_id(database: Session):

        last_appointment = AppointmentRepository.get_last_appointment(database)

        if not last_appointment:
            return "APT00000001"

        last_number = int(last_appointment.appointment_id[3:])
        return f"APT{last_number + 1:08d}"

    @staticmethod
    def create_appointment(
        database: Session,
        data: AppointmentCreate,
        created_by: int,
    ):

        patient = PatientRepository.get_active_patient_by_id(
            database,
            data.patient_id
        )

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        doctor = DoctorRepository.get_doctor_by_id(
            database,
            data.doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        if data.appointment_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment date cannot be in the past"
            )

        if (
            data.appointment_date == date.today()
            and data.appointment_time < datetime.now().time()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment time cannot be in the past"
            )

        slot = AppointmentRepository.get_doctor_slot(
            database=database,
            doctor_id=doctor.id,
            appointment_date=data.appointment_date,
            appointment_time=data.appointment_time,
        )

        if slot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor already has an appointment at this time"
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

        appointment = AppointmentRepository.create_appointment(
            database,
            appointment
        )

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment.appointment_id
        )

        return AppointmentService.serialize_appointment(
            appointment
        )
    @staticmethod
    def get_all_appointments(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
        doctor_id: str | None = None,
        patient_id: str | None = None,
        appointment_status: AppointmentStatus | None = None,
        appointment_date=None,
    ):

        doctor_db_id = None
        patient_db_id = None

        if doctor_id:
            doctor = DoctorRepository.get_doctor_by_id(
                database,
                doctor_id
            )

            if not doctor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor not found"
                )

            doctor_db_id = doctor.id

        if patient_id:
            patient = PatientRepository.get_active_patient_by_id(
                database,
                patient_id
            )

            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient not found"
                )

            patient_db_id = patient.id

        appointments, total = AppointmentRepository.get_all_appointments(
            database=database,
            page=page,
            limit=limit,
            search=search,
            doctor_id=doctor_db_id,
            patient_id=patient_db_id,
            appointment_status=appointment_status,
            appointment_date=appointment_date,
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "appointments": [
                AppointmentService.serialize_appointment(i)
                for i in appointments
            ],
        }

    @staticmethod
    def get_appointment_by_id(
        database: Session,
        appointment_id: str,
    ):

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment_id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )

        return AppointmentService.serialize_appointment(
            appointment
        )

    @staticmethod
    def update_appointment(
        database: Session,
        appointment_id: str,
        data: AppointmentUpdate,
    ):

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment_id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )

        update_data = data.model_dump(exclude_unset=True)

        if (
            "appointment_date" in update_data
            or "appointment_time" in update_data
        ):

            appointment_date = update_data.get(
                "appointment_date",
                appointment.appointment_date,
            )

            appointment_time = update_data.get(
                "appointment_time",
                appointment.appointment_time,
            )

            slot = AppointmentRepository.get_doctor_slot(
                database=database,
                doctor_id=appointment.doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            )

            if slot and slot.id != appointment.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Doctor already has an appointment at this time",
                )

        for key, value in update_data.items():
            setattr(appointment, key, value)

        appointment = AppointmentRepository.update_appointment(
            database,
            appointment,
        )

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment.appointment_id,
        )

        return AppointmentService.serialize_appointment(
            appointment
        )

    @staticmethod
    def delete_appointment(
        database: Session,
        appointment_id: str,
    ):

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment_id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )

        appointment = AppointmentRepository.delete_appointment(
            database,
            appointment,
        )

        return AppointmentService.serialize_appointment(
            appointment
        )

    @staticmethod
    def restore_appointment(
        database: Session,
        appointment_id: str,
    ):

        appointment = AppointmentRepository.get_any_appointment(
            database,
            appointment_id,
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )

        if appointment.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment is already active",
            )

        appointment = AppointmentRepository.restore_appointment(
            database,
            appointment,
        )

        appointment = AppointmentRepository.get_appointment_by_id(
            database,
            appointment.appointment_id,
        )

        return AppointmentService.serialize_appointment(
            appointment
        )