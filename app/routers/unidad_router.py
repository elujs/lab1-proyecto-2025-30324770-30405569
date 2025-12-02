# app/routers/unidad_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.unidad import UnidadAtencion
from app.schemas.unidad_schema import UnidadCreate, UnidadResponse, UnidadUpdate
from typing import List
from app.dependencies import requires_admin, requires_auth

router = APIRouter()

@router.post(
    "/unidades", 
    response_model=UnidadResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def create_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    nueva_unidad = UnidadAtencion(**unidad.model_dump())
    db.add(nueva_unidad)
    db.commit()
    db.refresh(nueva_unidad) 
    return nueva_unidad

@router.get(
    "/unidades/{unidad_id}", 
    response_model=UnidadResponse,
    dependencies=[Depends(requires_auth)]
)
def get_unidad(unidad_id: str, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada.")
    return unidad

@router.get(
    "/unidades", 
    response_model=List[UnidadResponse],
    dependencies=[Depends(requires_auth)]
)
def list_unidades(db: Session = Depends(get_db)):
    return db.query(UnidadAtencion).all()

@router.patch(
    "/unidades/{unidad_id}", 
    response_model=UnidadResponse,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def update_unidad(unidad_id: str, updates: UnidadUpdate, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada.")

    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(unidad, key, value)
    
    db.add(unidad)
    db.commit()
    db.refresh(unidad)
    return unidad

@router.delete(
    "/unidades/{unidad_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requires_admin)] # <-- Solo Admin
)
def delete_unidad(unidad_id: str, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada.")

    unidad.estado = "inactivo" 
    db.add(unidad)
    db.commit()
    return