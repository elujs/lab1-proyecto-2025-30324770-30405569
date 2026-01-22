from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.unidad_schema import UnidadCreate, UnidadResponse, UnidadUpdate
from app.dependencies import requires_admin, requires_auth
from app.services import unidad_service

router = APIRouter()

@router.post("/unidades", response_model=UnidadResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(requires_admin)])
def create_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    return unidad_service.create_unidad(db, unidad)

@router.get("/unidades/{unidad_id}", response_model=UnidadResponse, dependencies=[Depends(requires_auth)])
def get_unidad(unidad_id: str, db: Session = Depends(get_db)):
    return unidad_service.get_unidad(db, unidad_id)

@router.get("/unidades", response_model=List[UnidadResponse], dependencies=[Depends(requires_auth)])
def list_unidades(db: Session = Depends(get_db)):
    return unidad_service.list_unidades(db)

@router.patch("/unidades/{unidad_id}", response_model=UnidadResponse, dependencies=[Depends(requires_admin)])
def update_unidad(unidad_id: str, updates: UnidadUpdate, db: Session = Depends(get_db)):
    return unidad_service.update_unidad(db, unidad_id, updates)

@router.delete("/unidades/{unidad_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(requires_admin)])
def delete_unidad(unidad_id: str, db: Session = Depends(get_db)):
    unidad_service.delete_unidad(db, unidad_id)