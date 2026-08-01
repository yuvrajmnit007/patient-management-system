from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String

from app.models.doctor import Doctor, Department, Specialization


class DoctorRepository:

    @staticmethod
    def create_doctor(database: Session, doctor: Doctor):
        database.add(doctor)
        database.commit()
        database.refresh(doctor)
        return doctor

    @staticmethod
    def update_doctor(database: Session, doctor: Doctor):
        database.commit()
        database.refresh(doctor)
        return doctor

    @staticmethod
    def get_last_doctor(database: Session):
        return (
            database.query(Doctor)
            .order_by(Doctor.id.desc())
            .first()
        )

    @staticmethod
    def get_by_email(database: Session, email: str):
        return (
            database.query(Doctor)
            .filter(
                Doctor.email == email,
                Doctor.is_active == True
            )
            .first()
        )

    @staticmethod
    def get_by_phone_number(database: Session, phone_number: str):
        return (
            database.query(Doctor)
            .filter(
                Doctor.phone_number == phone_number,
                Doctor.is_active == True
            )
            .first()
        )

    @staticmethod
    def get_doctor_by_id(database: Session, doctor_id: str):
        return (
            database.query(Doctor)
            .filter(
                Doctor.doctor_id == doctor_id,
                Doctor.is_active == True
            )
            .first()
        )

    @staticmethod
    def get_any_doctor(database: Session, doctor_id: str):
        return (
            database.query(Doctor)
            .filter(
                Doctor.doctor_id == doctor_id
            )
            .first()
        )

    @staticmethod
    def get_all_doctors(
        database: Session,
        page: int,
        limit: int,
        search: str | None = None,
        department: Department | None = None,
        specialization: Specialization | None = None,
    ):

        query = (
            database.query(Doctor)
            .filter(Doctor.is_active == True)
        )

        if search:
            query = query.filter(
                or_(
                    Doctor.doctor_id.ilike(f"%{search}%"),
                    Doctor.full_name.ilike(f"%{search}%"),
                    Doctor.phone_number.ilike(f"%{search}%"),
                    Doctor.email.ilike(f"%{search}%"),
                    Doctor.qualification.ilike(f"%{search}%"),
                    Doctor.availability.ilike(f"%{search}%"),
                    cast(Doctor.department, String).ilike(f"%{search}%"),
                    cast(Doctor.specialization, String).ilike(f"%{search}%"),
                )
            )

        if department:
            query = query.filter(
                Doctor.department == department
            )

        if specialization:
            query = query.filter(
                Doctor.specialization == specialization
            )

        total = query.count()

        doctors = (
            query
            .order_by(Doctor.id)
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return doctors, total

    @staticmethod
    def delete_doctor(database: Session, doctor: Doctor):
        doctor.is_active = False
        database.commit()
        database.refresh(doctor)
        return doctor

    @staticmethod
    def restore_doctor(database: Session, doctor: Doctor):
        doctor.is_active = True
        database.commit()
        database.refresh(doctor)
        return doctor