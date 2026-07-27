from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password,verify_password,create_access_token


class UserService:

    @staticmethod
    def register(database: Session, data: UserCreate):

        existing = UserRepository.get_by_email(database, data.email)
        existing_phone = UserRepository.get_by_phone_number(database, data.phone_number)
        existing_username = UserRepository.get_by_username(database, data.username)


        if existing:
            raise ValueError("Email already exists")

        if existing_username:
            raise ValueError("Username already exists")

        if existing_phone:
            raise ValueError("Phone number already exists")

        user = User(
            full_name=data.full_name,
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            phone_number=data.phone_number
        )

        return UserRepository.create(database, user)


    @staticmethod
    def login(database : Session,data :UserLogin):
        user = UserRepository.get_by_email(database, data.email)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(data.password, user.password):
            raise ValueError("Invalid email or password")

        access_token=create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}