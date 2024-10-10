from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import licencias
from .core.db import check_and_create_tables

app = FastAPI()

# Configuración CORS (si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas estáticas para HTML
app.mount("/static", StaticFiles(directory="licencia_score/app/templates"), name="static")

# Ejecutar chequeo y creación de tablas al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    await check_and_create_tables()

# Incluir los endpoints
app.include_router(licencias.router, prefix="/suseso/api/licenciasv1")
