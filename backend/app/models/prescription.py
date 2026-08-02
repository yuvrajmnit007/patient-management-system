from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    prescription_id = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        unique=True,
        nullable=False,
    )

    diagnosis = Column(
        Text,
        nullable=False,
    )

    advice = Column(
        Text,
        nullable=True,
    )

    follow_up_date = Column(
        Date,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships

    appointment = relationship(
        "Appointment",
        foreign_keys=[appointment_id],
    )

    created_by_user = relationship(
        "User",
        foreign_keys=[created_by],
    )

    prescription_items = relationship(
        "PrescriptionItem",
        back_populates="prescription",
        cascade="all, delete-orphan",
    )