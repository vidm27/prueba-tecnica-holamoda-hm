from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.funcionalidades.autenticacion.esquemas import Token
from app.nucleo.config import config
from app.nucleo.limitador import limitador
from app.nucleo.seguridad import credenciales_validas, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token, summary="Obtener un token JWT",
             responses={429: {"description": "Demasiados intentos desde esta IP; ver cabecera Retry-After"}})
@limitador.limit(config.login_limite)  # exige el parámetro `request`
def login(request: Request, formulario: OAuth2PasswordRequestForm = Depends()):
    if not credenciales_validas(formulario.username, formulario.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario o clave incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=crear_token(formulario.username), expira_en_minutos=config.jwt_minutos)
