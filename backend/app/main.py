import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import literal, select
from sqlmodel import Session

from app.api import api
from app.nucleo.config import config
from app.nucleo.db import obtener_sesion
from app.nucleo.limitador import limitador
from app.nucleo.manejo_errores import registrar_manejadores

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
app.state.limitador = limitador
registrar_manejadores(app)


@app.get("/salud", tags=["Sistema"], summary="Estado del servicio")
def salud(sesion: Session = Depends(obtener_sesion)):
    sesion.execute(select(literal(1)))
    return {"estado": "ok"}


app.include_router(api)
