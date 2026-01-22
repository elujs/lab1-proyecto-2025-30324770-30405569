# Plataforma API para Gestión de Servicios Médicos 🏥

API RESTful desarrollada con **FastAPI** y **PostgreSQL** para la gestión integral de centros médicos. Permite administrar pacientes, médicos, agendas, citas y registros clínicos.

🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura en capas (Controladores, Servicios, Repositorios) construida sobre FastAPI.

# Diagrama de Arquitectura
Backend en FastAPI conectado a PostgreSQL, gestionado vía Docker

## Integrantes
* *Eduardo Lucena* - C.I: 30.324.770
* *Clara Peña*- C.I: 30.405.569


##  Cómo ejecutar el proyecto

### Opción A: Con Docker (Recomendada) 
Si tienes Docker instalado:

```bash
##Construir la imagen (solo la primera vez): docker compose up --build

##Detener el programa: docker compose down o control + c

##Ejecutar el programa (segunda vez en adelante): docker compose up

El server se abrira en:
http://localhost:8000
con la documentacion en:
http://localhost:8000/api_docs


## Opción B: Manualmente (Local) 🛠️
Crear entorno virtual: python -m venv venv

## Activar entorno: .\venv\Scripts\activate

## Instalar dependencias: pip install -r requirements.txt

## Configurar el archivo .env con tus credenciales de BD.

## Ejecutar: uvicorn app.main:app --reload

El server se abrira en:
http://127.0.0.1:8000
con la documentacion en:
http://127.0.0.1:8000/api_docs



# Credenciales seed
Al iniciar el proyecto con `seed.py`, se crean los siguientes usuarios por defecto para pruebas:

| Rol | Usuario | Contraseña | Permisos Principales |
| **Administrador** | `admin` | `admin123` | Gestión total (Usuarios, Unidades, Profesionales). |
| **Médico** | `medico` | `medico123` | Gestión clínica (Historias, Recetas). |

#Roles 
Administración: Encargado de la configuración (Sedes, Personal).

Profesional: Personal médico (Médicos, Enfermeras) con acceso a historias clínicas.

Cajero: Encargado de facturación y admisión de pacientes.

Auditor: Acceso de solo lectura a registros.

## ⚙️ Variables de Entorno (.env)

Si ejecutas el proyecto manualmente, crea un archivo `.env` en la raíz con las siguientes variables:
"
# Configuración de Seguridad 
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/lab1_db
SECRET_KEY=tu_clave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"

## 🛡️ Pruebas de Calidad (Pytest)

El proyecto incluye pruebas de integración. Para ejecutarlas, detén `uvicorn` y corre el siguiente comando en la raíz del proyecto:

python -m pytest