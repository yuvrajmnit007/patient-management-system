from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id"), nullable=False,
    )

    medicine_name = Column(String(150), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)
    duration = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    prescription = relationship(
        "Prescription",
        back_populates="prescription_items",
    )