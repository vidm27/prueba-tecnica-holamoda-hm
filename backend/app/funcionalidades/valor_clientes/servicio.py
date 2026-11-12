from sqlalchemy import case, func, select
from sqlmodel import Session

from app.nucleo.consultas import filas, redondear
from app.nucleo.modelos import Cliente

GASTO = Cliente.gasto_anual_estimado


class ValorClientesServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def segmentacion(self) -> dict:
        total = self._sesion.scalar(select(func.sum(GASTO)))
        niveles = filas(self._sesion, select(
            Cliente.nivel_valor.label("nivel"),
            func.count(Cliente.id).label("clientes"),
            func.sum(GASTO).label("gasto_anual_total"),
            func.min(GASTO).label("gasto_minimo"),
            func.max(GASTO).label("gasto_maximo"),
        ).group_by(Cliente.nivel_valor).order_by(func.min(GASTO)))
        for n in niveles:
            n["pct_gasto"] = redondear(100.0 * n["gasto_anual_total"] / total, 1)
            n["gasto_anual_total"] = redondear(n["gasto_anual_total"], 2)
            n["gasto_minimo"] = redondear(n["gasto_minimo"], 2)
            n["gasto_maximo"] = redondear(n["gasto_maximo"], 2)
        return {"pareto_top20_pct_gasto": self._pareto(), "niveles": niveles}

    def _pareto(self) -> float:
        """Porcentaje del gasto que aporta el 20% de clientes con mayor gasto (regla 80/20)."""
        ranking = select(
            GASTO.label("gasto"),
            func.row_number().over(order_by=GASTO.desc()).label("posicion"),
            func.count().over().label("total"),
        ).subquery()
        aporte_top = func.sum(case((ranking.c.posicion <= 0.2 * ranking.c.total, ranking.c.gasto), else_=0))
        pct = self._sesion.scalar(select(100.0 * aporte_top / func.sum(ranking.c.gasto)).select_from(ranking))
        return redondear(pct, 1)
