import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.nucleo.config import config
from app.nucleo.errores import TokenInvalido

ALGORITMO = "HS256"
esquema_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def credenciales_validas(usuario: str, clave: str) -> bool:
    # Comparación en tiempo constante; `&` evita cortocircuito que filtre cuál falló.
    # ponytail: un solo usuario definido en .env; tabla de usuarios + hash (bcrypt) si hubiera más.
    return (secrets.compare_digest(usuario.encode(), config.admin_usuario.encode())
            & secrets.compare_digest(clave.encode(), config.admin_clave.encode()))


def crear_token(usuario: str, minutos: int | None = None) -> str:
    vence = datetime.now(timezone.utc) + timedelta(minutes=config.jwt_minutos if minutos is None else minutos)
    return jwt.encode({"sub": usuario, "exp": vence}, config.jwt_secreto, algorithm=ALGORITMO)


def usuario_actual(token: str | None = Depends(esquema_oauth)) -> str:
    if token is None:
        raise TokenInvalido("Falta el token de acceso")
    try:
        return jwt.decode(token, config.jwt_secreto, algorithms=[ALGORITMO],
                          options={"require": ["exp", "sub"]})["sub"]
    except jwt.PyJWTError as e:
        raise TokenInvalido() from e
