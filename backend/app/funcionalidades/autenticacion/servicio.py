from app.funcionalidades.autenticacion.esquemas import Token
from app.nucleo.config import config
from app.nucleo.seguridad import credenciales_validas, crear_token


class CredencialesInvalidas(Exception):
    """El usuario o la clave no coinciden."""


class AutenticacionServicio:
    def iniciar_sesion(self, usuario: str, clave: str) -> Token:
        if not credenciales_validas(usuario, clave):
            raise CredencialesInvalidas
        return Token(access_token=crear_token(usuario), expira_en_minutos=config.jwt_minutos)
