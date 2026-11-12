from collections import Counter

from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas
from app.nucleo.modelos import Cliente, Compra

SEGMENTOS = {
    "nivel_valor": Cliente.nivel_valor,
    "grupo_edad": Cliente.grupo_edad,
    "genero": Cliente.genero,
}


class EnviosServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def por_segmento(self, segmento: str) -> list[dict]:
        """Reparto de tipos de envío dentro de cada segmento de clientes."""
        columna = SEGMENTOS[segmento]  # validado por la ruta: nunca llega un nombre arbitrario
        filas_envio = filas(self._sesion, compras_con_detalle(
            columna.label("segmento"), Compra.tipo_envio, func.count(Compra.id).label("compras"),
        ).group_by(columna, Compra.tipo_envio))

        total = Counter()
        for f in filas_envio:
            total[f["segmento"]] += f["compras"]
        for f in filas_envio:
            f["pct_segmento"] = round(100.0 * f["compras"] / total[f["segmento"]], 1)
        return sorted(filas_envio, key=lambda f: (f["segmento"], -f["pct_segmento"]))
