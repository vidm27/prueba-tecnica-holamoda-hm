from collections import defaultdict

from scipy.stats import kruskal
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle
from app.nucleo.modelos import Cliente, Compra, Producto

# Listas blancas: las columnas salen de aquí, nunca de texto libre del usuario.
METRICAS = {"monto_usd": Compra.monto_usd, "calificacion": Compra.calificacion}
VARIABLES = {
    "genero": Cliente.genero, "suscrito": Cliente.suscrito, "grupo_edad": Cliente.grupo_edad,
    "estado": Cliente.ubicacion, "nivel_valor": Cliente.nivel_valor, "frecuencia": Cliente.frecuencia_compras,
    "categoria": Producto.categoria, "producto": Producto.nombre, "talla": Compra.talla, "color": Compra.color,
    "temporada": Compra.temporada, "tipo_envio": Compra.tipo_envio, "metodo_pago": Compra.metodo_pago,
    "descuento": Compra.descuento,
}
# Número de pruebas posibles: base de la corrección de Bonferroni.
PRUEBAS_POSIBLES = len(METRICAS) * len(VARIABLES)


class DatosInsuficientes(Exception):
    """No hay variación suficiente para comparar los grupos."""


def _etiqueta(valor) -> str:
    if isinstance(valor, bool):  # mismo formato que el texto de PostgreSQL: true / false
        return "true" if valor else "false"
    return str(valor)


class HipotesisServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def probar(self, metrica: str, variable: str) -> dict:
        """Kruskal-Wallis de `metrica` entre los grupos de `variable`, con corrección de Bonferroni."""
        filas = self._sesion.execute(compras_con_detalle(
            VARIABLES[variable].label("grupo"), METRICAS[metrica].label("valor"),
        )).all()
        grupos = defaultdict(list)
        for grupo, valor in filas:
            grupos[_etiqueta(grupo)].append(valor)
        ordenados = sorted(grupos.items())

        try:
            estadistico, p = kruskal(*[valores for _, valores in ordenados])
        except ValueError as e:
            raise DatosInsuficientes from e
        ajustado = min(1.0, float(p) * PRUEBAS_POSIBLES)

        if ajustado < 0.05:
            veredicto = "Diferencia estadísticamente significativa, incluso corrigiendo por comparaciones múltiples."
        elif p < 0.05:
            veredicto = ("Parece significativa pero NO sobrevive la corrección por comparaciones múltiples: "
                         "probable falso positivo.")
        else:
            veredicto = "Sin evidencia de diferencia entre los grupos."
        return {
            "metrica": metrica, "variable": variable, "prueba": "Kruskal-Wallis",
            "estadistico": float(estadistico), "p_valor": float(p), "p_ajustado": ajustado,
            "significativo": ajustado < 0.05, "veredicto": veredicto,
            "grupos": [{"grupo": g, "n": len(v), "media": sum(v) / len(v)} for g, v in ordenados],
        }
