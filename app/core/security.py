from pwdlib import PasswordHash
from uuid import UUID
import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
from app.core.exceptions import InvalidTokenError

password_hasher = PasswordHash.recommended()



def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()

    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256"
    )

def decode_access_token(token: str) -> dict:
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"]
        )
        
        return payload
    except jwt.InvalidTokenError:
        raise InvalidTokenError(detail="Некоректный JWT") from None