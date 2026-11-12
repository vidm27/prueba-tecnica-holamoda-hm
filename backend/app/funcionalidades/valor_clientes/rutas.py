from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.valor_clientes.esquemas import Valor
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Valor de clientes"])


@router.get("/clientes/valor", response_model=Valor, summary="Segmentación de clientes por valor")
def valor_clientes(con: Connection = Depends(obtener_conexion)):
    niveles = filas(con, """
        SELECT nivel_valor AS nivel, count(*) AS clientes,
               round(sum(gasto_anual_estimado)::numeric, 2) AS gasto_anual_total,
               round((100.0 * sum(gasto_anual_estimado) / sum(sum(gasto_anual_estimado)) OVER ())::numeric, 1) AS pct_gasto,
               min(gasto_anual_estimado) AS gasto_minimo, max(gasto_anual_estimado) AS gasto_maximo
        FROM clientes GROUP BY nivel_valor ORDER BY gasto_minimo""")
    pareto = filas(con, """
        SELECT round((100.0 * sum(g) FILTER (WHERE rn <= 0.2 * n) / sum(g))::numeric, 1) AS pct
        FROM (SELECT gasto_anual_estimado AS g,
                     row_number() OVER (ORDER BY gasto_anual_estimado DESC) AS rn,
                     count(*) OVER () AS n FROM clientes) t""")[0]["pct"]
    return {"pareto_top20_pct_gasto": pareto, "niveles": niveles}
