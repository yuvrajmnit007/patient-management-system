from enum import Enum

from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    ForeignKey, DateTime, func, Enum as SqlEnum,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class Specialization(str, Enum):
    CARDIOLOGY = "Cardiology"
    DERMATOLOGY = "Dermatology"
    NEUROLOGY = "Neurology"
    PEDIATRICS = "Pediatrics"
    ORTHOPEDICS = "Orthopedics"
    GYNECOLOGY = "Gynecology"
    PSYCHIATRY = "Psychiatry"
    ONCOLOGY = "Oncology"
    RADIOLOGY = "Radiology"
    UROLOGY = "Urology"
    GASTROENTEROLOGY = "Gastroenterology"
    GENERAL_PHYSICIAN = "General Physician"


class Department(str, Enum):
    MEDICINE = "Medicine"
    SURGERY = "Surgery"
    EMERGENCY = "Emergency"
    ICU = "ICU"
    ENT = "ENT"
    OPD = "OPD"
    RADIOLOGY = "Radiology"
    ORTHOPEDICS = "Orthopedics"


class DoctorStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


def _values(obj):
    return [e.value for e in obj]


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)

    specialization = Column(
        SqlEnum(Specialization, name="doctor_specialization", values_callable=_values),
        nullable=False,
    )
    department = Column(
        SqlEnum(Department, name="doctor_department", values_callable=_values),
        nullable=False,
    )

    qualification = Column(String(150), nullable=False)
    experience = Column(Integer, nullable=False)
    consultation_fee = Column(Float, nullable=False)
    availability = Column(Text, nullable=True)

    phone_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    address = Column(Text, nullable=True)

    is_active = Column(Boolean, default=False, nullable=False)

    status = Column(
        SqlEnum(DoctorStatus, name="doctor_status", values_callable=_values),
        default=DoctorStatus.PENDING,
        nullable=False,
    )

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_user = relationship("User", foreign_keys=[created_by])

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)
    user = relationship("User", foreign_keys=[user_id], backref="doctor_profile")

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False,
        server_default=func.now(), onupdate=func.now(),
    )