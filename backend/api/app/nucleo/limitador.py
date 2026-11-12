from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Clave = IP del cliente. No se confía en X-Forwarded-For (es falsificable);
# detrás de un proxy propio habría que configurarlo.
# ponytail: contadores en memoria por proceso; con varias réplicas usar storage_uri="redis://...".
limitador = Limiter(key_func=get_remote_address)


def respuesta_limite_excedido(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    espera = exc.limit.limit.get_expiry()  # cota superior: tamaño de la ventana
    return JSONResponse(
        status_code=429,
        content={"detail": f"Demasiados intentos. Intenta de nuevo en {espera} segundos."},
        headers={"Retry-After": str(espera)},
    )
