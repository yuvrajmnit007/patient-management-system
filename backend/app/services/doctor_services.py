from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.doctor import Doctor, Department, Specialization
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:

    @staticmethod
    def generate_doctor_id(database: Session):

        last_doctor = DoctorRepository.get_last_doctor(database)

        if not last_doctor:
            return "DOC00000001"

        last_number = int(last_doctor.doctor_id[3:])
        return f"DOC{last_number + 1:08d}"

    @staticmethod
    def create_doctor(
        database: Session,
        data: DoctorCreate,
        created_by: int
    ):

        if data.email:
            if DoctorRepository.get_by_email(database, data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

        if DoctorRepository.get_by_phone_number(database, data.phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists"
            )

        doctor = Doctor(
            doctor_id=DoctorService.generate_doctor_id(database),
            full_name=data.full_name,
            specialization=data.specialization,
            department=data.department,
            qualification=data.qualification,
            experience=data.experience,
            consultation_fee=data.consultation_fee,
            availability=data.availability,
            phone_number=data.phone_number,
            email=data.email,
            address=data.address,
            is_active=True,
            created_by=created_by
        )

        return DoctorRepository.create_doctor(database, doctor)

    @staticmethod
    def get_all_doctors(
        database: Session,
        page: int,
        limit: int,
        search: str | None,
        department: str | None,
        specialization: str | None,
    ):

        if department:
            try:
                department = Department[
                    department.strip().replace(" ", "_").upper()
                ]
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid department"
                )

        if specialization:
            try:
                specialization = Specialization[
                    specialization.strip().replace(" ", "_").upper()
                ]
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid specialization"
                )

        doctors, total = DoctorRepository.get_all_doctors(
            database=database,
            page=page,
            limit=limit,
            search=search,
            department=department,
            specialization=specialization
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "doctors": doctors
        }

    @staticmethod
    def get_doctor_by_id(
        database: Session,
        doctor_id: str
    ):

        doctor = DoctorRepository.get_doctor_by_id(
            database,
            doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        return doctor

    @staticmethod
    def update_doctor(
        database: Session,
        doctor_id: str,
        data: DoctorUpdate
    ):

        doctor = DoctorRepository.get_doctor_by_id(
            database,
            doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        if (
            data.email
            and data.email != doctor.email
        ):
            if DoctorRepository.get_by_email(database, data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

        if (
            data.phone_number
            and data.phone_number != doctor.phone_number
        ):
            if DoctorRepository.get_by_phone_number(
                database,
                data.phone_number
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already exists"
                )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(doctor, key, value)

        return DoctorRepository.update_doctor(
            database,
            doctor
        )

    @staticmethod
    def delete_doctor(
        database: Session,
        doctor_id: str
    ):

        doctor = DoctorRepository.get_doctor_by_id(
            database,
            doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        return DoctorRepository.delete_doctor(
            database,
            doctor
        )

    @staticmethod
    def restore_doctor(
        database: Session,
        doctor_id: str
    ):

        doctor = DoctorRepository.get_any_doctor(
            database,
            doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        if doctor.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor is already active"
            )

        return DoctorRepository.restore_doctor(
            database,
            doctor
        )