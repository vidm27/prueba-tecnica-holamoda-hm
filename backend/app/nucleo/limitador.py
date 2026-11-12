from slowapi import Limiter
from slowapi.util import get_remote_address

# Clave = IP del cliente. No se confía en X-Forwarded-For (es falsificable);
# detrás de un proxy propio habría que configurarlo.
# ponytail: contadores en memoria por proceso; con varias réplicas usar storage_uri="redis://...".
limitador = Limiter(key_func=get_remote_address)
