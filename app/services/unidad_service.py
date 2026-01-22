from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.unidad import UnidadAtencion
from app.schemas.unidad_schema import UnidadCreate, UnidadUpdate

def create_unidad(db: Session, unidad: UnidadCreate):
    new_unidad = UnidadAtencion(**unidad.model_dump())
    db.add(new_unidad)
    db.commit()
    db.refresh(new_unidad) 
    return new_unidad

def get_unidad(db: Session, unidad_id: str):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada.")
    return unidad

def list_unidades(db: Session):
    return db.query(UnidadAtencion).all()

def update_unidad(db: Session, unidad_id: str, updates: UnidadUpdate):
    unidad = get_unidad(db, unidad_id)
    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(unidad, key, value)
    db.commit()
    db.refresh(unidad)
    return unidad

def delete_unidad(db: Session, unidad_id: str):
    unidad = get_unidad(db, unidad_id)
    unidad.estado = "inactivo" 
    db.commit()
    return unidad