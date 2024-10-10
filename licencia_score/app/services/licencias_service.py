import io
import pandas as pd
from fastapi import UploadFile
from ..models.licencias import Licencias,DatosAdicionales
from ..core.config import SessionLocal
from sqlalchemy.orm import Session
from licencia_score.app.repository.licencias_repository import get_top_licencias
import io
import pandas as pd
from fastapi import UploadFile
from ..models.licencias import Licencias, DatosAdicionales
from ..core.config import SessionLocal
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

def process_row(row, db: Session):
    # Guardar en Licencias
    licencia = Licencias(
        propensity_score_rn=float(row.get("propensity_score_rn", 0)) if row.get("propensity_score_rn") else 0,
        propensity_score_rn2=float(row.get("propensity_score_rn2", 0)) if row.get("propensity_score_rn2") else 0,
        propensity_score_frecuencia_mensual=float(row.get("propensity_score_frecuencia_mensual", 1.0)) if row.get("propensity_score_frecuencia_mensual") else 1.0,
        propensity_score_frecuencia_semanal=float(row.get("propensity_score_frecuencia_semanal", 1.0)) if row.get("propensity_score_frecuencia_semanal") else 1.0,
        propensity_score_otorgados_mensual=float(row.get("propensity_score_otorgados_mensual", 1.0)) if row.get("propensity_score_otorgados_mensual") else 1.0,
        propensity_score_otorgados_semanal=float(row.get("propensity_score_otorgados_semanal", 1.0)) if row.get("propensity_score_otorgados_semanal") else 1.0,
        propensity_score_ml=float(row.get("propensity_score_ml", 0.0)) if row.get("propensity_score_ml") else 0.0,
        propensity_score=float(row.get("propensity_score", 0.0)) if row.get("propensity_score") else 0.0,
    )
    db.add(licencia)
    db.commit() 
    
    # Se permite hacer la adición de datos adicionales
    for key, value in row.items():
        print(f"DatosAdicionales = Key: {key}, Value: {value} \n")
        datos_adicionales = DatosAdicionales(
            licencia_id=licencia.id,
            nombre_campo=key,
            valor=value
        )
        db.add(datos_adicionales)
        db.commit() 

async def process_file(file: UploadFile):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    futures = []
    
    # Conectar a la base de datos
    with ThreadPoolExecutor() as executor:
        for index, row in df.iterrows():
            # Crear una nueva sesión para cada fila
            db = SessionLocal()
            #process_row(row,db)
            futures.append(executor.submit(process_row, row, db))

        for future in futures:
            try:
                future.result()  # Esperar a que se complete la tarea
            except Exception as e:
                db.rollback()  # Hacer rollback en caso de error
                raise e
            finally:
                db.commit()  # Commit después de procesar cada fila
                db.close()   # Cerrar la sesión

async def fetch_top_licencias(db: Session, limit: int = 100, order: str = "desc"):    
    order_desc = (order.lower() == "desc")
    return get_top_licencias(db, limit=limit, order_desc=order_desc)

