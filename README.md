# Plataforma API para Gestión de Servicios Médicos 🏥

API RESTful desarrollada con **FastAPI** y **PostgreSQL** para la gestión integral de centros médicos. Permite administrar pacientes, médicos, agendas, citas y registros clínicos.

## Integrantes
* *Eduardo Lucena* - C.I: 30.324.770
* *Clara Peña*- C.I: 30.405.569

##  Cómo ejecutar el proyecto

### Opción A: Con Docker (Recomendada) 
Si tienes Docker instalado, solo necesitas ejecutar un comando:

```bash
docker compose up --build

## Opción B: Manualmente (Local) 🛠️
Crear entorno virtual: python -m venv venv

## Activar entorno: .\venv\Scripts\activate

## Instalar dependencias: pip install -r requirements.txt

## Configurar el archivo .env con tus credenciales de BD.

## Ejecutar: uvicorn app.main:app --reload