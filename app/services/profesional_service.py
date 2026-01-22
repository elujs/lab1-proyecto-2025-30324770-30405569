from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.profesional import Profesional
from app.schemas.profesional_schema import ProfesionalCreate, ProfesionalUpdate

def create_profesional(db: Session, profesional: ProfesionalCreate):
    # Regla: Unicidad del registro profesional
    existing = db.query(Profesional).filter(
        Profesional.registro_profesional == profesional.registro_profesional
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registro profesional ya existe.")

    new_profesional = Profesional(**profesional.model_dump())
    db.add(new_profesional)
    db.commit()
    db.refresh(new_profesional) 
    return new_profesional

def get_profesional(db: Session, profesional_id: str):
    profesional = db.query(Profesional).filter(Profesional.id == profesional_id).first()
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado.")
    return profesional

def list_profesionales(db: Session):
    return db.query(Profesional).all()

def update_profesional(db: Session, profesional_id: str, updates: ProfesionalUpdate):
    profesional = get_profesional(db, profesional_id)
    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(profesional, key, value)
    db.commit()
    db.refresh(profesional)
    return profesional

def delete_profesional(db: Session, profesional_id: str):
    profesional = get_profesional(db, profesional_id)
    profesional.estado = "inactivo" 
    db.commit()
    return profesional