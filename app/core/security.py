from datetime import datetime, timedelta

from passlib.context import CryptContext
import jwt

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    exp = datetime.now() + timedelta(minutes=settings.JWT_TOKEN_EXP)
    jwt_form = {"sub": sub, "exp": exp}
    encoded_jwt = jwt.encode(
        payload=jwt_form, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
    except jwt.exceptions.InvalidTokenError:
        return None
    return payload
