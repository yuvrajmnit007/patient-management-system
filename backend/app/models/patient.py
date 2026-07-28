from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy import DateTime,func
from app.models.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"



class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"




class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    blood_group = Column(String(10), nullable=True)
    phone_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_number = Column(String)
    allergies = Column(Text)
    medical_history = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by=Column(Integer, ForeignKey("users.id"), nullable=True)
    creator=relationship("User", back_populates="patients_created", foreign_keys=[created_by])
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())