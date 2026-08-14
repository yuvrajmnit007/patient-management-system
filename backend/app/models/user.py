from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, DateTime, Boolean, func, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            name="user_role",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    patients_created = relationship(
        "Patient", back_populates="creator", foreign_keys="[Patient.created_by]"
    )