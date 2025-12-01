from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.persona import PersonaAtendida
from app.schemas.persona_schema import PersonaCreate, PersonaResponse, PersonaUpdate
from typing import List

router = APIRouter()

# 1. POST /personas: Crea una nueva persona (Paciente)
@router.post("/personas", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    # Lógica 1: Buscar si el documento ya existe (Validación de Unicidad)
    documento_existente = db.query(PersonaAtendida).filter(
        PersonaAtendida.numero_documento == persona.numero_documento
    ).first()
    
    if documento_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El número de documento ya está registrado."
        )

    # 2. Crear la instancia del modelo SQLAlchemy con los datos validados
    nueva_persona = PersonaAtendida(**persona.model_dump())

    # 3. Guardar en BD
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona) 

    return nueva_persona

# 2. GET /personas/{id}: Obtiene una persona por ID
@router.get("/personas/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: str, db: Session = Depends(get_db)):
    # Lógica: Buscar por ID
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada."
        )
    
    return persona


# 3. GET /personas: Obtiene lista de personas (Implementación simple)
# NOTA: El RF pide filtros (documento/edad/sexo) y paginación.
# Por ahora, implementamos la lista completa. Los filtros se añaden después.
@router.get("/personas", response_model=List[PersonaResponse])
def list_personas(db: Session = Depends(get_db)):
    personas = db.query(PersonaAtendida).all()
    return personas


# 4. PATCH /personas/{id}: Actualiza datos (parcialmente)
@router.patch("/personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: str, updates: PersonaUpdate, db: Session = Depends(get_db)):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada.")

    # Convertir el Pydantic model a un diccionario, omitiendo los campos None
    update_data = updates.model_dump(exclude_unset=True) 

    # Aplicar las actualizaciones al objeto de SQLAlchemy
    for key, value in update_data.items():
        setattr(persona, key, value)
    
    # Guardar en BD
    db.add(persona)
    db.commit()
    db.refresh(persona)
    
    return persona


# 5. DELETE /personas/{id}: Eliminación Lógica
@router.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: str, db: Session = Depends(get_db)):
    persona = db.query(PersonaAtendida).filter(PersonaAtendida.id == persona_id).first()
    
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada.")

    # Eliminación Lógica (cambia el estado, no borra el registro)
    persona.estado = "inactivo" 

    # Guardar en BD
    db.add(persona)
    db.commit()
    
    # Retornar 204 No Content (exitoso sin devolver un cuerpo)
    return