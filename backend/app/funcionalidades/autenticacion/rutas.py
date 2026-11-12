from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.funcionalidades.autenticacion.esquemas import Token
from app.funcionalidades.autenticacion.servicio import AutenticacionServicio, CredencialesInvalidas
from app.funcionalidades.autenticacion.dependencias import obtener_servicio
from app.nucleo.config import config
from app.nucleo.limitador import limitador

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token, summary="Obtener un token JWT",
             responses={429: {"description": "Demasiados intentos desde esta IP; ver cabecera Retry-After"}})
@limitador.limit(config.login_limite)  # slowapi exige el parámetro `request`
def login(request: Request, formulario: OAuth2PasswordRequestForm = Depends(),
          servicio: AutenticacionServicio = Depends(obtener_servicio)):
    try:
        return servicio.iniciar_sesion(formulario.username, formulario.password)
    except CredencialesInvalidas:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario o clave incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})
