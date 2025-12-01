# app/routers/unidad_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.unidad import UnidadAtencion
from app.schemas.unidad_schema import UnidadCreate, UnidadResponse, UnidadUpdate
from typing import List

router = APIRouter()

# 1. POST /unidades: Crea una nueva unidad de atención
@router.post("/unidades", response_model=UnidadResponse, status_code=status.HTTP_201_CREATED)
def create_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    # Nota: No se requiere unicidad más allá del ID, se pueden tener varias unidades con el mismo nombre
    
    # 1. Crear la instancia del modelo SQLAlchemy
    nueva_unidad = UnidadAtencion(**unidad.model_dump())

    # 2. Guardar en BD
    db.add(nueva_unidad)
    db.commit()
    db.refresh(nueva_unidad) 

    return nueva_unidad

# 2. GET /unidades/{id}: Obtiene por ID
@router.get("/unidades/{unidad_id}", response_model=UnidadResponse)
def get_unidad(unidad_id: str, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de atención no encontrada."
        )
    
    return unidad

# 3. GET /unidades: Obtiene lista
@router.get("/unidades", response_model=List[UnidadResponse])
def list_unidades(db: Session = Depends(get_db)):
    unidades = db.query(UnidadAtencion).all()
    return unidades

# 4. PATCH /unidades/{id}: Actualiza datos (parcialmente)
@router.patch("/unidades/{unidad_id}", response_model=UnidadResponse)
def update_unidad(unidad_id: str, updates: UnidadUpdate, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    
    if not unidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada.")

    update_data = updates.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
        setattr(unidad, key, value)
    
    db.add(unidad)
    db.commit()
    db.refresh(unidad)
    
    return unidad

# 5. DELETE /unidades/{id}: Eliminación Lógica
@router.delete("/unidades/{unidad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unidad(unidad_id: str, db: Session = Depends(get_db)):
    unidad = db.query(UnidadAtencion).filter(UnidadAtencion.id == unidad_id).first()
    
    if not unidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada.")

    unidad.estado = "inactivo" 

    db.add(unidad)
    db.commit()
    
    return