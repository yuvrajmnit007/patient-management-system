from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserService:

    @staticmethod
    def register(database: Session, data: UserCreate):

        existing = UserRepository.get_by_email(database, data.email)

        if existing:
            raise ValueError("Email already exists")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
        )

        return UserRepository.create(database, user)