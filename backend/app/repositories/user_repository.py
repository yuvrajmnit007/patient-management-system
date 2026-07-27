from squlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_by_email(database:Session ,email:str):
        return database.query(User).filter(User.email == email).first()


    @staticmethod
    def create(database:Session, user:User):
        database.add(user)
        database.commit()
        database.refresh(user)
        return user