from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.doctor import Doctor, Department, DoctorStatus, Specialization
from app.models.user import User, UserRole
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.user_repository import UserRepository
from app.schemas.doctor import DoctorRegister, DoctorUpdate


class DoctorService:

    @staticmethod
    def generate_doctor_id(database: Session) -> str:
        last = DoctorRepository.get_last_doctor(database)
        if not last:
            return "DOC00000001"
        return f"DOC{int(last.doctor_id[3:]) + 1:08d}"

    @staticmethod
    def register_doctor(database: Session, doctor: DoctorRegister) -> Doctor:
        if UserRepository.get_by_email(database, doctor.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
        if UserRepository.get_by_phone_number(database, doctor.phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists",
            )

        try:
            user = User(
                full_name=doctor.full_name,
                username=doctor.email,
                email=doctor.email,
                phone_number=doctor.phone_number,
                password=hash_password(doctor.password),
                role=UserRole.DOCTOR,
                is_active=False,
            )
            user = UserRepository.create(database, user)

            new_doctor = Doctor(
                doctor_id=DoctorService.generate_doctor_id(database),
                full_name=doctor.full_name,
                user_id=user.id,
                specialization=doctor.specialization,
                department=doctor.department,
                qualification=doctor.qualification,
                experience=doctor.experience,
                consultation_fee=doctor.consultation_fee,
                availability=doctor.availability,
                phone_number=doctor.phone_number,
                email=doctor.email,
                address=doctor.address,
                status=DoctorStatus.PENDING,
                is_active=False,
                created_by=None,
            )
            return DoctorRepository.create_doctor(database, new_doctor)

        except Exception:
            database.rollback()
            raise

    @staticmethod
    def get_all_doctors(
        database: Session,
        page: int,
        limit: int,
        search: str | None,
        department: str | None,
        specialization: str | None,
    ) -> dict:
        if department:
            try:
                department = Department[
                    department.strip().replace(" ", "_").upper()
                ]
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid department",
                )
        if specialization:
            try:
                specialization = Specialization[
                    specialization.strip().replace(" ", "_").upper()
                ]
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid specialization",
                )

        doctors, total = DoctorRepository.get_all_doctors(
            database=database, page=page, limit=limit,
            search=search, department=department, specialization=specialization,
        )
        return {
            "items": doctors,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit if limit else 0,
        }

    @staticmethod
    def get_doctor_by_id(database: Session, doctor_id: str) -> Doctor:
        doctor = DoctorRepository.get_doctor_by_id(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )
        return doctor

    @staticmethod
    def update_doctor(
        database: Session, doctor_id: str, data: DoctorUpdate
    ) -> Doctor:
        doctor = DoctorRepository.get_doctor_by_id(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )

        if data.email and data.email != doctor.email:
            existing = DoctorRepository.get_by_email(database, data.email)
            if existing and existing.id != doctor.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )
        if data.phone_number and data.phone_number != doctor.phone_number:
            existing = DoctorRepository.get_by_phone_number(database, data.phone_number)
            if existing and existing.id != doctor.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already exists",
                )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(doctor, key, value)
        return DoctorRepository.update_doctor(database, doctor)

    @staticmethod
    def delete_doctor(database: Session, doctor_id: str) -> Doctor:
        doctor = DoctorRepository.get_doctor_by_id(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )
        return DoctorRepository.delete_doctor(database, doctor)

    @staticmethod
    def restore_doctor(database: Session, doctor_id: str) -> Doctor:
        doctor = DoctorRepository.get_any_doctor(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )
        if doctor.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is already active",
            )
        return DoctorRepository.restore_doctor(database, doctor)

    @staticmethod
    def get_pending_doctors(database: Session) -> list[Doctor]:
        return DoctorRepository.get_pending_doctors(database)

    @staticmethod
    def approve_doctor(
        database: Session, doctor_id: str, current_user_id: int
    ) -> Doctor:
        doctor = DoctorRepository.get_any_doctor(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )
        if doctor.status == DoctorStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is already approved",
            )

        user = (
            UserRepository.get_by_id(database, doctor.user_id)
            if doctor.user_id else None
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account for doctor not found",
            )

        doctor.status = DoctorStatus.APPROVED
        doctor.is_active = True
        doctor.created_by = current_user_id
        user.is_active = True
        database.commit()
        database.refresh(doctor)
        return doctor

    @staticmethod
    def reject_doctor(database: Session, doctor_id: str) -> Doctor:
        doctor = DoctorRepository.get_any_doctor(database, doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
            )
        if doctor.status == DoctorStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is already rejected",
            )

        user = (
            UserRepository.get_by_id(database, doctor.user_id)
            if doctor.user_id else None
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account for doctor not found",
            )

        doctor.status = DoctorStatus.REJECTED
        doctor.is_active = False
        user.is_active = False
        database.commit()
        database.refresh(doctor)
        return doctor

@staticmethod
def get_current_doctor(database: Session, current_user_id: int) -> Doctor:
    doctor = DoctorRepository.get_by_user_id(database, current_user_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No doctor profile linked to this account",
        )
    return doctor

