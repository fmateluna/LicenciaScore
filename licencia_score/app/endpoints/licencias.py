 
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from licencia_score.app.core.config import SessionLocal
from licencia_score.app.services.licencias_service import fetch_top_licencias
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from ..services.licencias_service import process_file

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/licencias/")
async def get_licencias(total: int = 100, order: str = "mayor", db: Session = Depends(get_db)):
    #if pass_key != "Licencias2024":
    #    raise HTTPException(status_code=401, detail="Unauthorized")
    return await fetch_top_licencias(db, limit=total, order=order)

@router.get("/", response_class=HTMLResponse)
async def upload_file_form():
    return HTMLResponse(open("licencia_score/app/templates/upload.html").read())

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    # Procesar el archivo
    await process_file(file)
    return {"message": "Archivo subido y procesado exitosamente"}