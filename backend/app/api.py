"""Router central de la API: todos los endpoints cuelgan de aquí.

- `publica`: solo el login (emite el token).
- `protegida`: el resto. Lleva la dependencia de autenticación una sola vez, así que una ruta
  nueva queda protegida por defecto; para hacerla pública tendría que ir fuera de `protegida`.
"""
from fastapi import APIRouter, Depends

from app.funcionalidades.autenticacion import rutas as autenticacion
from app.funcionalidades.calidad import rutas as calidad
from app.funcionalidades.compras import rutas as compras
from app.funcionalidades.envios import rutas as envios
from app.funcionalidades.estacionalidad import rutas as estacionalidad
from app.funcionalidades.estados import rutas as estados
from app.funcionalidades.hipotesis import rutas as hipotesis
from app.funcionalidades.promociones import rutas as promociones
from app.funcionalidades.resumen import rutas as resumen
from app.funcionalidades.satisfaccion import rutas as satisfaccion
from app.funcionalidades.suscripcion import rutas as suscripcion
from app.funcionalidades.tallas import rutas as tallas
from app.funcionalidades.valor_clientes import rutas as valor_clientes
from app.nucleo.seguridad import usuario_actual

PROTEGIDAS = (calidad, compras, envios, estacionalidad, estados, hipotesis,
              promociones, resumen, satisfaccion, suscripcion, tallas, valor_clientes)

publica = APIRouter()
publica.include_router(autenticacion.router)

protegida = APIRouter(dependencies=[Depends(usuario_actual)])
for funcionalidad in PROTEGIDAS:
    protegida.include_router(funcionalidad.router)

api = APIRouter(prefix="/api/v1")
api.include_router(publica)
api.include_router(protegida)
