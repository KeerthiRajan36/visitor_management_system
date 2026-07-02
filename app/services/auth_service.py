from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import LoginRequest

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt import create_access_token


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user: UserCreate
    ):

        username_exists = db.query(User).filter(
            User.username == user.username
        ).first()

        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )

        email_exists = db.query(User).filter(
            User.email == user.email
        ).first()

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )

        db_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            role=user.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def login(
        db: Session,
        login_data: LoginRequest
    ):

        user = db.query(User).filter(
            User.username == login_data.username
        ).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password."
            )

        if not verify_password(
            login_data.password,
            user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password."
            )

        token = create_access_token(
            {
                "sub": user.username,
                "role": user.role.value
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }