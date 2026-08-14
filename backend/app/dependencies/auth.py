from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.oauth2 import oauth2_scheme
from app.core.security import decode_access_token
from app.database.database import get_db
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository


_CREDENTIAL_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise _CREDENTIAL_EXC

    email = payload.get("sub")
    if email is None:
        raise _CREDENTIAL_EXC

    user = UserRepository.get_by_email(db, email)
    if user is None:
        raise _CREDENTIAL_EXC

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive",
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def require_doctor(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor access required",
        )
    return current_user