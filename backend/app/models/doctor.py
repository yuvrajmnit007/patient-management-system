from enum import Enum
from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime , Enum as SqlEnum,func, ForeignKey
from app.models.base import Base


class Specilazation(str, Enum):
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


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(SqlEnum(Specilazation), nullable=False)
    department = Column(SqlEnum(Department), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())