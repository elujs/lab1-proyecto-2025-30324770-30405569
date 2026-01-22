from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.persona import PersonaAtendida
from app.schemas.persona_schema import PersonaCreate, PersonaUpdate

def create_persona(db: Session, persona: PersonaCreate):
    # Regla: Verificación de duplicidad por número de documento
    existing = db.query(PersonaAtendida).filter(
        PersonaAtendida.numero_documento == persona.numero_documento
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El documento ya existe.")

    new_persona = PersonaAtendida(**persona.model_dump())
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona) 
    return new_persona

def get_persona(db: Session, persona_id: str):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada.")
    return persona

def list_personas(db: Session):
    return db.query(PersonaAtendida).all()

def update_persona(db: Session, persona_id: str, updates: PersonaUpdate):
    persona = get_persona(db, persona_id)
    update_data = updates.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(persona, key, value)
    db.commit()
    db.refresh(persona)
    return persona

def delete_persona(db: Session, persona_id: str):
    persona = get_persona(db, persona_id)
    # Regla: Baja lógica (estado inactivo)
    persona.estado = "inactivo" 
    db.commit()
    return persona