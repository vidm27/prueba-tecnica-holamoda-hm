from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from scipy.stats import kruskal
from sqlalchemy import Connection

from app.funcionalidades.hipotesis.esquemas import ResultadoHipotesis
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Hipótesis"])

# Listas blancas: los nombres de columna salen de aquí, nunca del usuario.
METRICAS = {"monto_usd": "c.monto_usd", "calificacion": "c.calificacion"}
VARIABLES = {
    "genero": "cl.genero", "suscrito": "cl.suscrito::text", "grupo_edad": "cl.grupo_edad",
    "estado": "cl.ubicacion", "nivel_valor": "cl.nivel_valor", "frecuencia": "cl.frecuencia_compras",
    "categoria": "p.categoria", "producto": "p.nombre", "talla": "c.talla", "color": "c.color",
    "temporada": "c.temporada", "tipo_envio": "c.tipo_envio", "metodo_pago": "c.metodo_pago",
    "descuento": "c.descuento::text",
}
PRUEBAS_POSIBLES = len(METRICAS) * len(VARIABLES)  # base de la corrección de Bonferroni

Metrica = Literal["monto_usd", "calificacion"]
Variable = Literal["genero", "suscrito", "grupo_edad", "estado", "nivel_valor", "frecuencia", "categoria",
                   "producto", "talla", "color", "temporada", "tipo_envio", "metodo_pago", "descuento"]


@router.get("/hipotesis", response_model=ResultadoHipotesis,
            summary="¿Cambia la métrica según la variable? (Kruskal-Wallis con corrección)")
def probar_hipotesis(metrica: Metrica, variable: Variable, con: Connection = Depends(obtener_conexion)):
    grupos = filas(con, f"""
        SELECT {VARIABLES[variable]} AS grupo, array_agg({METRICAS[metrica]}) AS valores
        FROM compras c JOIN productos p ON p.id = c.producto_id JOIN clientes cl ON cl.id = c.cliente_id
        GROUP BY 1 ORDER BY 1""")
    try:
        estadistico, p = kruskal(*[g["valores"] for g in grupos])
    except ValueError:
        raise HTTPException(422, "No hay variación suficiente para comparar los grupos")
    ajustado = min(1.0, float(p) * PRUEBAS_POSIBLES)
    if ajustado < 0.05:
        veredicto = "Diferencia estadísticamente significativa, incluso corrigiendo por comparaciones múltiples."
    elif p < 0.05:
        veredicto = ("Parece significativa pero NO sobrevive la corrección por comparaciones múltiples: "
                     "probable falso positivo.")
    else:
        veredicto = "Sin evidencia de diferencia entre los grupos."
    return {"metrica": metrica, "variable": variable, "prueba": "Kruskal-Wallis",
            "estadistico": float(estadistico), "p_valor": float(p), "p_ajustado": ajustado,
            "significativo": ajustado < 0.05, "veredicto": veredicto,
            "grupos": [{"grupo": g["grupo"], "n": len(g["valores"]),
                        "media": sum(g["valores"]) / len(g["valores"])} for g in grupos]}
