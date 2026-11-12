import time
from collections import defaultdict, deque
from math import ceil
from threading import Lock

from app.nucleo.config import config


class LimitadorIntentos:
    """Ventana deslizante de intentos fallidos por clave, en memoria.

    ponytail: el estado es por proceso; con varios workers o réplicas hay que moverlo a Redis.
    """

    LIMITE_CLAVES = 10_000  # tope de memoria: al superarlo se purgan las claves vencidas

    def __init__(self, maximo: int, ventana: int, reloj=time.monotonic):
        self.maximo, self.ventana, self.reloj = maximo, ventana, reloj
        self._fallos: dict[str, deque[float]] = defaultdict(deque)
        self._cerrojo = Lock()

    def _podar(self, clave: str) -> deque[float]:
        fallos = self._fallos[clave]
        while fallos and fallos[0] <= self.reloj() - self.ventana:
            fallos.popleft()
        return fallos

    def segundos_de_espera(self, clave: str) -> int:
        """0 si puede intentar; si no, segundos hasta que venza el fallo más antiguo."""
        with self._cerrojo:
            fallos = self._podar(clave)
            if len(fallos) < self.maximo:
                if not fallos:
                    self._fallos.pop(clave, None)
                return 0
            return max(1, ceil(fallos[0] + self.ventana - self.reloj()))

    def registrar_fallo(self, clave: str) -> None:
        with self._cerrojo:
            if len(self._fallos) > self.LIMITE_CLAVES:
                for k in list(self._fallos):
                    if not self._podar(k):
                        del self._fallos[k]
            self._fallos[clave].append(self.reloj())

    def olvidar(self, clave: str) -> None:
        with self._cerrojo:
            self._fallos.pop(clave, None)

    def reiniciar(self) -> None:
        with self._cerrojo:
            self._fallos.clear()


# Por IP (frena a un atacante) y por usuario (frena ataques repartidos entre muchas IPs;
# umbral más alto para que no sea fácil bloquear a un usuario legítimo).
por_ip = LimitadorIntentos(config.login_max_fallos_ip, config.login_ventana_seg)
por_usuario = LimitadorIntentos(config.login_max_fallos_usuario, config.login_ventana_seg)
