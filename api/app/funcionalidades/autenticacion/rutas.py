from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.funcionalidades.autenticacion.esquemas import Token
from app.nucleo import limitador
from app.nucleo.config import config
from app.nucleo.seguridad import credenciales_validas, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token, summary="Obtener un token JWT",
             responses={429: {"description": "Demasiados intentos fallidos; ver cabecera Retry-After"}})
def login(request: Request, formulario: OAuth2PasswordRequestForm = Depends()):
    # No se confía en X-Forwarded-For (es falsificable); detrás de un proxy propio habría que configurarlo.
    ip = request.client.host if request.client else "desconocida"
    usuario = formulario.username.lower()

    # El bloqueo se evalúa antes de mirar la clave: así un bloqueado no puede seguir adivinando.
    espera = max(limitador.por_ip.segundos_de_espera(ip), limitador.por_usuario.segundos_de_espera(usuario))
    if espera:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                            f"Demasiados intentos fallidos. Intenta de nuevo en {espera} segundos.",
                            headers={"Retry-After": str(espera)})

    if not credenciales_validas(formulario.username, formulario.password):
        limitador.por_ip.registrar_fallo(ip)
        limitador.por_usuario.registrar_fallo(usuario)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario o clave incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})

    limitador.por_ip.olvidar(ip)
    return Token(access_token=crear_token(formulario.username), expira_en_minutos=config.jwt_minutos)
