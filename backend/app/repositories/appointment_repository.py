from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.appointment import Appointment, AppointmentStatus


class AppointmentRepository:

    @staticmethod
    def create_appointment(database: Session, appointment: Appointment) -> Appointment:
        database.add(appointment)
        database.commit()
        database.refresh(appointment)
        return appointment

    @staticmethod
    def update_appointment(database: Session, appointment: Appointment) -> Appointment:
        database.commit()
        database.refresh(appointment)
        return appointment

    @staticmethod
    def get_last_appointment(database: Session) -> Appointment | None:
        return database.query(Appointment).order_by(Appointment.id.desc()).first()

    @staticmethod
    def get_appointment_by_id(
        database: Session, appointment_id: str
    ) -> Appointment | None:
        return (
            database.query(Appointment)
            .options(
                joinedload(Appointment.patient),
                joinedload(Appointment.doctor),
            )
            .filter(
                Appointment.appointment_id == appointment_id,
                Appointment.is_active == True,
            )
            .first()
        )

    @staticmethod
    def get_any_appointment(
        database: Session, appointment_id: str
    ) -> Appointment | None:
        return (
            database.query(Appointment)
            .filter(Appointment.appointment_id == appointment_id)
            .first()
        )

    @staticmethod
    def get_doctor_slot(
        database: Session,
        doctor_id: int,
        appointment_date,
        appointment_time,
    ) -> Appointment | None:
        return (
            database.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time,
                Appointment.is_active == True,
                Appointment.status != AppointmentStatus.CANCELLED,
            )
            .first()
        )

    @staticmethod
    def get_all_appointments(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
        doctor_id: int | None = None,
        patient_id: int | None = None,
        status: AppointmentStatus | None = None,
        appointment_date: date | None = None,
    ) -> tuple[list[Appointment], int]:
        query = (
            database.query(Appointment)
            .options(
                joinedload(Appointment.patient),
                joinedload(Appointment.doctor),
            )
            .filter(Appointment.is_active == True)
        )

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Appointment.appointment_id.ilike(pattern),
                    Appointment.reason.ilike(pattern),
                )
            )

        if doctor_id:
            query = query.filter(Appointment.doctor_id == doctor_id)
        if patient_id:
            query = query.filter(Appointment.patient_id == patient_id)
        if status:
            query = query.filter(Appointment.status == status)
        if appointment_date:
            query = query.filter(Appointment.appointment_date == appointment_date)

        total = query.count()
        appointments = (
            query.order_by(
                Appointment.appointment_date.desc(),
                Appointment.appointment_time.desc(),
            )
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return appointments, total

    @staticmethod
    def delete_appointment(
        database: Session, appointment: Appointment
    ) -> Appointment:
        appointment.is_active = False
        database.commit()
        database.refresh(appointment)
        return appointment

    @staticmethod
    def restore_appointment(
        database: Session, appointment: Appointment
    ) -> Appointment:
        appointment.is_active = True
        database.commit()
        database.refresh(appointment)
        return appointment