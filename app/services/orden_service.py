from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.orden import Orden, Prescripcion, Resultado
from app.models.episodio import EpisodioAtencion
from app.schemas.orden_schema import OrdenCreate, PrescripcionCreate, ResultadoCreate

def emitir_orden(db: Session, data: OrdenCreate):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == data.episodio_id).first()
    if not episodio or episodio.estado == "cerrado":
        raise HTTPException(status_code=400, detail="Episodio no válido o cerrado")
    
    nueva_orden = Orden(**data.model_dump())
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden

def emitir_prescripcion(db: Session, data: PrescripcionCreate):
    episodio = db.query(EpisodioAtencion).filter(EpisodioAtencion.id == data.episodio_id).first()
    if not episodio or episodio.estado == "cerrado":
        raise HTTPException(status_code=400, detail="Episodio no válido o cerrado")
        
    nueva_p = Prescripcion(**data.model_dump())
    db.add(nueva_p)
    db.commit()
    db.refresh(nueva_p)
    return nueva_p

def registrar_resultado(db: Session, data: ResultadoCreate):
    orden = db.query(Orden).filter(Orden.id == data.orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Versionado (RF 2.4)
    ultima_version = db.query(Resultado).filter(Resultado.orden_id == data.orden_id).count()
    nuevo_res = Resultado(**data.model_dump(), version=ultima_version + 1)
    
    # Al recibir resultado, podemos marcar la orden como completada
    orden.estado = "completada"
    
    db.add(nuevo_res)
    db.commit()
    db.refresh(nuevo_res)
    return nuevo_res