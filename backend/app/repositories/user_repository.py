from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def create(database: Session, user: User) -> User:
        database.add(user)
        database.commit()
        database.refresh(user)
        return user

    @staticmethod
    def get_by_id(database: Session, user_id: int) -> User | None:
        return database.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(database: Session, email: str) -> User | None:
        return database.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(database: Session, username: str) -> User | None:
        return database.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_phone_number(database: Session, phone_number: str) -> User | None:
        return database.query(User).filter(User.phone_number == phone_number).first()