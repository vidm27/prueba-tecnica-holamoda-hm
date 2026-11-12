import pytest

from app.funcionalidades.autenticacion.servicio import AutenticacionServicio, CredencialesInvalidas
from app.nucleo.config import config


def test_credenciales_invalidas_lanzan_error_de_dominio():
    with pytest.raises(CredencialesInvalidas):
        AutenticacionServicio().iniciar_sesion("nadie", "incorrecta")


def test_emite_token_con_credenciales_validas():
    token = AutenticacionServicio().iniciar_sesion(config.admin_usuario, config.admin_clave)
    assert token.token_type == "bearer" and token.expira_en_minutos == config.jwt_minutos
