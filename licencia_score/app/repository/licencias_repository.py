 
from sqlalchemy.orm import Session
from licencia_score.app.models.licencias import Licencias, DatosAdicionales

def get_top_licencias_only_score(db: Session, limit: int, order_desc: bool = True):
    query = db.query(Licencias)
    if order_desc:
        query = query.order_by(Licencias.propensity_score.desc())
    else:
        query = query.order_by(Licencias.propensity_score)
    return query.limit(limit).all()


def get_top_licencias(db: Session, limit: int, order_desc: bool = True):
    # Definir el orden de las columnas de forma secuencial
    if order_desc:
        query = db.query(Licencias).order_by(
            Licencias.propensity_score.asc(),
            Licencias.propensity_score_rn.asc(),
            Licencias.propensity_score_otorgados_mensual.asc(),
            Licencias.propensity_score_frecuencia_mensual.asc(),
            Licencias.propensity_score_frecuencia_semanal.asc(),
            Licencias.propensity_score_otorgados_semanal.asc(),
            Licencias.propensity_score_ml.asc(),  
            Licencias.propensity_score_rn2.asc(),
        )
    else:
        query = db.query(Licencias).order_by(
            Licencias.propensity_score.asc(),
            Licencias.propensity_score_rn.asc(),
            Licencias.propensity_score_otorgados_mensual.asc(),
            Licencias.propensity_score_frecuencia_mensual.asc(),
            Licencias.propensity_score_frecuencia_semanal.asc(),
            Licencias.propensity_score_otorgados_semanal.asc(),
            Licencias.propensity_score_ml.asc(),  
            Licencias.propensity_score_rn2.asc(),
        )
    
    licencias = query.limit(limit).all()

    # Lista donde guardaremos las licencias con el campo "info" agregado
    result = []

    # Iteramos sobre cada licencia para obtener sus datos adicionales
    for licencia in licencias:
        # Obtenemos los datos adicionales relacionados con la licencia
        datos_adicionales = db.query(DatosAdicionales).filter(DatosAdicionales.licencia_id == licencia.id).all()

        # Creamos un diccionario donde almacenamos los datos adicionales como "info"
        info = {}
        for dato in datos_adicionales:
            info[dato.nombre_campo] = dato.valor

        # Convertimos la licencia a un diccionario y agregamos el campo "info"
        licencia_dict = {
            "propensity_score": licencia.propensity_score,
            "propensity_score_ml": licencia.propensity_score_ml,
            "id": licencia.id,
            "propensity_score_rn": licencia.propensity_score_rn,
            "propensity_score_rn2": licencia.propensity_score_rn2,
            "propensity_score_frecuencia_mensual": licencia.propensity_score_frecuencia_mensual,
            "propensity_score_frecuencia_semanal": licencia.propensity_score_frecuencia_semanal,
            "propensity_score_otorgados_mensual": licencia.propensity_score_otorgados_mensual,
            "propensity_score_otorgados_semanal": licencia.propensity_score_otorgados_semanal,
            # Agregamos el diccionario "info" con los datos adicionales
            "info": info
        }

        # Añadimos la licencia completa al resultado final
        result.append(licencia_dict)

    return result
