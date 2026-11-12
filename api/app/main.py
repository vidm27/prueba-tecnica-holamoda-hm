import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import Connection, text
from sqlalchemy.exc import SQLAlchemyError

from app.funcionalidades.autenticacion import rutas as autenticacion
from app.funcionalidades.compras import rutas as compras
from app.funcionalidades.estacionalidad import rutas as estacionalidad
from app.funcionalidades.estados import rutas as estados
from app.funcionalidades.promociones import rutas as promociones
from app.funcionalidades.resumen import rutas as resumen
from app.funcionalidades.satisfaccion import rutas as satisfaccion
from app.funcionalidades.tallas import rutas as tallas
from app.nucleo.config import config
from app.nucleo.db import obtener_conexion
from app.nucleo.seguridad import usuario_actual

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("api")

app = FastAPI(
    title="Tendencias de compra · Hola Moda",
    description="API de analítica sobre el dataset Customer Shopping Trends. "
                "Obtén un token en `/api/v1/auth/login` y úsalo con el botón **Authorize**.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=config.cors_origenes.split(","),
                   allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])


@app.exception_handler(SQLAlchemyError)
async def error_bd(_: Request, exc: SQLAlchemyError):
    log.exception("Error de base de datos")
    return JSONResponse(status_code=503, content={"detail": "Base de datos no disponible"})


@app.get("/salud", tags=["Sistema"], summary="Estado del servicio")
def salud(con: Connection = Depends(obtener_conexion)):
    con.execute(text("SELECT 1"))
    return {"estado": "ok"}


# Cada funcionalidad es una rebanada vertical: ruta + esquemas + SQL + tests en su carpeta.
app.include_router(autenticacion.router, prefix="/api/v1")  # público: emite el token
for rebanada in (compras, estacionalidad, estados, promociones, resumen, satisfaccion, tallas):
    app.include_router(rebanada.router, prefix="/api/v1", dependencies=[Depends(usuario_actual)])
