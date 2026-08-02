from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Time, Date, func, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.models.base import Base


class AppointmentStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(String(20),unique=True,nullable=False,index=True,)
    patient_id = Column(Integer,ForeignKey("patients.id"),nullable=False,)
    doctor_id = Column(Integer,ForeignKey("doctors.id"),nullable=False,)
    appointment_date = Column(Date,nullable=False,)
    appointment_time = Column(Time,nullable=False,)
    reason = Column(Text,nullable=False,)
    notes = Column(Text,nullable=True,)
    status = Column(SqlEnum(AppointmentStatus),nullable=False,default=AppointmentStatus.PENDING,)
    is_active = Column(Boolean,default=True,)
    created_at = Column(DateTime,nullable=False,default=func.now(),)
    updated_at = Column(DateTime,nullable=False,default=func.now(),onupdate=func.now(),)
    created_by = Column(Integer,ForeignKey("users.id"),nullable=False,)
    patient = relationship("Patient",foreign_keys=[patient_id],)
    doctor = relationship("Doctor",foreign_keys=[doctor_id],)
    created_by_user = relationship("User",foreign_keys=[created_by],)