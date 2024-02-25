import jwt
import bcrypt

from src.configurations.settings import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):

    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )

    return decoded


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    )


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
