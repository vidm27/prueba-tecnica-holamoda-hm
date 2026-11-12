"""Reglas de calidad sobre el conjunto completo (no fila por fila).

Pydantic valida cada fila; estas reglas detectan problemas que solo se ven
mirando todas las filas juntas: redundancias, sesgos imposibles, ruido.
"""
from loguru import logger as log

import pandas as pd


MUESTRA_MINIMA = 100  # reglas estadísticas no se evalúan con menos filas
SINONIMOS_FRECUENCIA = [("Quarterly", "Every 3 Months"), ("Bi-Weekly", "Fortnightly")]


def _hallazgo(regla, descripcion, severidad, afectadas, total, **evidencia):
    return {"regla": regla, "descripcion": descripcion, "severidad": severidad,
            "filas_afectadas": int(afectadas), "total_filas": int(total), "evidencia": evidencia}


def columnas_redundantes(df):
    iguales = (df.descuento == df.codigo_promo).mean()
    if iguales == 1:
        return _hallazgo("columnas_redundantes",
                         "'descuento' y 'codigo_promo' son idénticas en todas las filas; aportan un solo dato.",
                         "media", len(df), len(df), coincidencia=1.0)


def beneficios_por_genero(df):
    tasas = df.groupby("genero")[["suscrito", "descuento"]].mean().round(3)
    sin_beneficio = tasas[(tasas.suscrito == 0) & (tasas.descuento == 0)].index.tolist()
    if sin_beneficio:
        afectadas = df.genero.isin(sin_beneficio).sum()
        return _hallazgo("beneficios_por_genero",
                         f"Ningún cliente de género {', '.join(sin_beneficio)} tiene suscripción ni descuento: "
                         "sesgo de origen en los datos, no un comportamiento real.",
                         "alta", afectadas, len(df), tasas=tasas.to_dict("index"))


def suscripcion_implica_descuento(df):
    suscritos = df[df.suscrito]
    if len(suscritos) and suscritos.descuento.all():
        return _hallazgo("suscripcion_implica_descuento",
                         "Todo cliente suscrito tiene descuento: las variables no son independientes.",
                         "media", len(suscritos), len(df))


def pago_preferido_aleatorio(df):
    if len(df) < MUESTRA_MINIMA:
        return None
    coincide = (df.metodo_pago == df.metodo_pago_preferido).mean()
    azar = 1 / df.metodo_pago.nunique()
    if abs(coincide - azar) < 0.03:
        return _hallazgo("pago_preferido_aleatorio",
                         "El método de pago 'preferido' coincide con el usado igual que el azar: no es informativo.",
                         "media", (df.metodo_pago != df.metodo_pago_preferido).sum(), len(df),
                         coincidencia=round(coincide, 3), esperado_por_azar=round(azar, 3))


def frecuencias_sinonimas(df):
    presentes = [par for par in SINONIMOS_FRECUENCIA if set(par) <= set(df.frecuencia_compras)]
    if presentes:
        afectadas = df.frecuencia_compras.isin([v for par in presentes for v in par]).sum()
        return _hallazgo("frecuencias_sinonimas",
                         "Categorías de frecuencia con el mismo significado; se unifican en 'compras_por_anio'.",
                         "info", afectadas, len(df), pares=presentes)


def frecuencia_sin_relacion_historial(df):
    if len(df) < MUESTRA_MINIMA:
        return None
    # Spearman = Pearson sobre rangos (evita depender de scipy).
    rho = df.compras_por_anio.rank().corr(df.compras_previas.rank())
    if abs(rho) < 0.1:
        return _hallazgo("frecuencia_sin_relacion_historial",
                         "La frecuencia declarada no se relaciona con las compras previas (p.ej. 'Weekly' con 1 compra previa).",
                         "media", len(df), len(df), spearman=round(rho, 3))


def distribuciones_uniformes(df, umbral_cv=0.15):
    """Datos reales rara vez son uniformes; conteos casi iguales por tramo sugieren datos sintéticos."""
    if len(df) < MUESTRA_MINIMA:
        return None
    uniformes = {}
    for col in ["edad", "monto_usd", "calificacion"]:
        conteos = pd.cut(df[col], bins=10).value_counts()
        cv = conteos.std() / conteos.mean()
        if cv < umbral_cv:
            uniformes[col] = round(cv, 3)
    if uniformes:
        return _hallazgo("distribuciones_uniformes",
                         "Distribuciones casi perfectamente uniformes: indicio de datos sintéticos.",
                         "info", len(df), len(df), coef_variacion_por_tramo=uniformes)


def sin_dimension_temporal(df):
    return _hallazgo("sin_dimension_temporal",
                     "El dataset no trae fecha de compra: no se pueden analizar tendencias en el tiempo ni recompra.",
                     "info", len(df), len(df))


REGLAS = [columnas_redundantes, beneficios_por_genero, suscripcion_implica_descuento,
          pago_preferido_aleatorio, frecuencias_sinonimas, frecuencia_sin_relacion_historial,
          distribuciones_uniformes, sin_dimension_temporal]


def auditar(df: pd.DataFrame) -> pd.DataFrame:
    hallazgos = []
    for regla in REGLAS:
        try:
            if h := regla(df):
                hallazgos.append(h)
        except Exception:  # una regla defectuosa no debe tumbar la carga
            log.exception("Regla de auditoría '{}' falló", regla.__name__)
    for h in hallazgos:
        log.info("Auditoría [{}] {}: {}/{} filas", h["severidad"], h["regla"], h["filas_afectadas"], h["total_filas"])
    return pd.DataFrame(hallazgos, columns=["regla", "descripcion", "severidad",
                                            "filas_afectadas", "total_filas", "evidencia"])
