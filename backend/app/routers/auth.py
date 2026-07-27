from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # dependency injection he ye
    try:
        new_user = UserService.register(db, user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/login",response_model=UserResponse)
def login_user(user:UserLogin, db: Session = Depends(get_db)):
    try:
        token = UserService.login(db, user)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))