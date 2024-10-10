 
from .config import Base, engine
from sqlalchemy import inspect
from licencia_score.app.models.licencias import Licencias, DatosAdicionales

async def check_and_create_tables():
    inspector = inspect(engine)
    with engine.connect() as conn:
        if not inspector.has_table("licencias"):
            Base.metadata.create_all(bind=engine, tables=[Licencias.__table__])
        if not inspector.has_table("datos_adicionales"):
            Base.metadata.create_all(bind=engine, tables=[DatosAdicionales.__table__])

check_and_create_tables()
