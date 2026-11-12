from loguru import logger

from app.funcionalidades.autenticacion.esquemas import Token
from app.nucleo.config import config
from app.nucleo.errores import CredencialesInvalidas
from app.nucleo.seguridad import credenciales_validas, crear_token


class AutenticacionServicio:
    def iniciar_sesion(self, usuario: str, clave: str) -> Token:
        if not credenciales_validas(usuario, clave):
            logger.warning("Intento de login con credenciales inválidas")  # sin usuario ni clave en el log
            raise CredencialesInvalidas
        return Token(access_token=crear_token(usuario), expira_en_minutos=config.jwt_minutos)
