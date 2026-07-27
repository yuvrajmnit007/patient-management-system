from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_by_email(database:Session ,email:str):
        return database.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_phone_number(database:Session ,phone_number:str):
        return database.query(User).filter(User.phone_number == phone_number).first()

    @staticmethod
    def get_by_username(database:Session ,username:str):
        return database.query(User).filter(User.username == username).first()

    

    @staticmethod
    def create(database:Session, user:User):
        database.add(user)
        database.commit()
        database.refresh(user)
        return user