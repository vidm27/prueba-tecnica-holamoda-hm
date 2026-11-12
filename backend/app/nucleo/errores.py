"""Errores de la aplicación. Cada uno lleva su código HTTP y un código estable para el cliente.

Los servicios los lanzan y deciden el estado y el mensaje; no conocen HTTP. Un único manejador
(nucleo/manejo_errores.py) los convierte en la respuesta estándar de la API.
"""


class ErrorAplicacion(Exception):
    estado: int = 500
    codigo: str = "error_interno"

    def __init__(self, mensaje: str, *, detalle: list[dict] | None = None,
                 cabeceras: dict[str, str] | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.detalle = detalle
        self.cabeceras = cabeceras or {}


class CredencialesInvalidas(ErrorAplicacion):
    estado, codigo = 401, "credenciales_invalidas"

    def __init__(self):
        super().__init__("Usuario o clave incorrectos", cabeceras={"WWW-Authenticate": "Bearer"})


class TokenInvalido(ErrorAplicacion):
    estado, codigo = 401, "token_invalido"

    def __init__(self, mensaje: str = "Token inválido o vencido"):
        super().__init__(mensaje, cabeceras={"WWW-Authenticate": "Bearer"})


class DatosInsuficientes(ErrorAplicacion):
    estado, codigo = 422, "datos_insuficientes"


class LimiteExcedido(ErrorAplicacion):
    estado, codigo = 429, "limite_excedido"

    def __init__(self, espera_seg: int):
        super().__init__(f"Demasiados intentos. Intenta de nuevo en {espera_seg} segundos.",
                         cabeceras={"Retry-After": str(espera_seg)})


class ServicioNoDisponible(ErrorAplicacion):
    estado, codigo = 503, "servicio_no_disponible"

    def __init__(self):
        super().__init__("Base de datos no disponible")
