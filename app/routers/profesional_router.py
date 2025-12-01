from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.profesional import Profesional
from app.schemas.profesional_schema import ProfesionalCreate, ProfesionalResponse, ProfesionalUpdate # <-- La línea de la importación
from typing import List

router = APIRouter()

# -----------------------------------------------------------------
# 1. POST /profesionales: Crea un nuevo profesional
# -----------------------------------------------------------------
@router.post("/profesionales", response_model=ProfesionalResponse, status_code=status.HTTP_201_CREATED)
def create_profesional(profesional: ProfesionalCreate, db: Session = Depends(get_db)):
    # 1. Validación de Unicidad: registro_profesional debe ser único
    registro_existente = db.query(Profesional).filter(
        Profesional.registro_profesional == profesional.registro_profesional
    ).first()
    
    if registro_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El número de registro profesional ya está registrado."
        )

    # 2. Crear la instancia del modelo SQLAlchemy
    nuevo_profesional = Profesional(**profesional.model_dump())

    # 3. Guardar en BD
    db.add(nuevo_profesional)
    db.commit()
    db.refresh(nuevo_profesional) 

    return nuevo_profesional

# -----------------------------------------------------------------
# 2. GET /profesionales/{id}: Obtiene por ID
# -----------------------------------------------------------------
@router.get("/profesionales/{profesional_id}", response_model=ProfesionalResponse)
def get_profesional(profesional_id: str, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    
    if not profesional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesional no encontrado."
        )
    
    return profesional

# -----------------------------------------------------------------
# 3. GET /profesionales: Obtiene lista
# -----------------------------------------------------------------
@router.get("/profesionales", response_model=List[ProfesionalResponse])
def list_profesionales(db: Session = Depends(get_db)):
    profesionales = db.query(Profesional).all()
    return profesionales

# -----------------------------------------------------------------
# 4. PATCH /profesionales/{id}: Actualiza datos (parcialmente)
# -----------------------------------------------------------------
@router.patch("/profesionales/{profesional_id}", response_model=ProfesionalResponse)
def update_profesional(profesional_id: str, updates: ProfesionalUpdate, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado.")

    # Convertir el Pydantic model a un diccionario, omitiendo los campos None
    update_data = updates.model_dump(exclude_unset=True) 

    # Aplicar las actualizaciones al objeto de SQLAlchemy
    for key, value in update_data.items():
        setattr(profesional, key, value)
    
    # Guardar en BD
    db.add(profesional)
    db.commit()
    db.refresh(profesional)
    
    return profesional

# -----------------------------------------------------------------
# 5. DELETE /profesionales/{id}: Eliminación Lógica
# -----------------------------------------------------------------
@router.delete("/profesionales/{profesional_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profesional(profesional_id: str, db: Session = Depends(get_db)):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado.")

    # Eliminación Lógica (cambia el estado, no borra el registro)
    profesional.estado = "inactivo" 

    # Guardar en BD
    db.add(profesional)
    db.commit()
    
    return