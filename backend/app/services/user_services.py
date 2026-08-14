from sqlalchemy.orm import Session

from app.core.security import (
    hash_password, verify_password, create_access_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class UserService:

    @staticmethod
    def register(database: Session, data: UserCreate) -> User:
        if UserRepository.get_by_email(database, data.email):
            raise ValueError("Email already exists")
        if UserRepository.get_by_username(database, data.username):
            raise ValueError("Username already exists")
        if UserRepository.get_by_phone_number(database, data.phone_number):
            raise ValueError("Phone number already exists")

        user = User(
            full_name=data.full_name,
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            phone_number=data.phone_number,
        )
        return UserRepository.create(database, user)

    @staticmethod
    def login(database: Session, data: UserLogin) -> dict:
        user = UserRepository.get_by_email(database, data.email)
        if not user or not verify_password(data.password, user.password):
            raise ValueError("Invalid email or password")
        if not user.is_active:
            raise ValueError(
                "Your account is inactive. Please contact the administrator."
            )

        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value}
        )
        return {"access_token": access_token, "token_type": "bearer"}