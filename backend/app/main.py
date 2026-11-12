import time
import uuid

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy import literal, select
from sqlmodel import Session

from app.api import api
from app.nucleo.config import config
from app.nucleo.db import obtener_sesion
from app.nucleo.documentacion import DESCRIPCION, TAGS
from app.nucleo.limitador import limitador
from app.nucleo.logs import configurar_logs
from app.nucleo.manejo_errores import registrar_manejadores

configurar_logs()

app = FastAPI(
    title="Tendencias de compra · Hola Moda",
    summary="Analítica de compras de moda: promociones, tallas, segmentos y calidad de datos.",
    description=DESCRIPCION,
    version="0.1.0",
    openapi_tags=TAGS,
    swagger_ui_parameters={"persistAuthorization": True, "displayRequestDuration": True},
)
app.add_middleware(CORSMiddleware, allow_origins=config.cors_origenes.split(","),
                   allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
app.state.limitador = limitador


@app.middleware("http")
async def registrar_peticion(request: Request, call_next):
    """Cada petición lleva un request_id (cabecera X-Request-ID o uno nuevo) y se registra con su duración."""
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
    inicio = time.perf_counter()
    with logger.contextualize(request_id=request_id):
        logger.debug("→ {} {}", request.method, request.url.path)
        respuesta = await call_next(request)
        ms = (time.perf_counter() - inicio) * 1000
        logger.info("{} {} → {} ({:.1f} ms)", request.method, request.url.path, respuesta.status_code, ms)
    respuesta.headers["X-Request-ID"] = request_id
    return respuesta
registrar_manejadores(app)


@app.get("/salud", tags=["Sistema"], summary="Estado del servicio")
def salud(sesion: Session = Depends(obtener_sesion)):
    """Confirma que la API responde y que la base de datos acepta consultas. Sin autenticación."""
    sesion.execute(select(literal(1)))
    return {"estado": "ok"}


app.include_router(api)
