from statistics import median

from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.promociones.esquemas import Promociones
from app.nucleo.db import filas, obtener_conexion
from app.nucleo.sql import UNIONES

router = APIRouter(tags=["Promociones"])


def recomendar(p: dict, mediana_ventas: float, mediana_calif: float) -> tuple[str, str]:
    vende_poco, gusta = p["ventas"] < mediana_ventas, p["calificacion"] >= mediana_calif
    if vende_poco and gusta:
        return "promocion_exposicion", "Bien calificado pero se vende poco: falta visibilidad, no precio."
    if vende_poco:
        return "revisar_producto", "Se vende poco y está mal calificado: descontar no resuelve el problema."
    if not gusta:
        return "riesgo_reputacion", "Se vende mucho pero está mal calificado."
    return "mantener", "Buen volumen y buena calificación."


@router.get("/productos/promocion", response_model=Promociones,
            summary="¿De qué producto lanzar una promoción?")
def promociones(con: Connection = Depends(obtener_conexion)):
    productos = filas(con, f"""
        SELECT p.nombre AS producto, p.categoria, count(*) AS ventas,
               round(avg(c.calificacion)::numeric, 2) AS calificacion,
               round(avg(c.descuento::int)::numeric, 3) AS pct_descuento,
               round(avg((cl.genero = 'Female')::int)::numeric, 3) AS pct_mujeres,
               round((avg(c.monto_usd) FILTER (WHERE c.descuento))::numeric, 2) AS ticket_con_descuento,
               round((avg(c.monto_usd) FILTER (WHERE NOT c.descuento))::numeric, 2) AS ticket_sin_descuento
        {UNIONES} GROUP BY p.nombre, p.categoria ORDER BY ventas, calificacion DESC""")
    m_ventas = median(p["ventas"] for p in productos)
    m_calif = float(median(p["calificacion"] for p in productos))
    for p in productos:
        p["recomendacion"], p["motivo"] = recomendar(p, m_ventas, m_calif)
    mujeres_desc = filas(con, f"SELECT count(*) AS n {UNIONES} WHERE cl.genero = 'Female' AND c.descuento")[0]["n"]
    return {"mediana_ventas": m_ventas, "mediana_calificacion": m_calif,
            "compras_mujeres_con_descuento": mujeres_desc,
            "advertencia": "Sin fecha de compra no se puede medir el efecto del descuento sobre el volumen de ventas.",
            "productos": productos}
