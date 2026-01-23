import sys
import os
from datetime import datetime, timedelta

# Asegurar que Python encuentre la carpeta 'app' para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.usuario import Usuario
from app.models.persona import PersonaAtendida
from app.models.profesional import Profesional
from app.models.unidad import UnidadAtencion
from app.models.agenda import Agenda
from app.models.cita import Cita
from app.models.episodio import EpisodioAtencion
from app.models.clinico import NotaClinica, Diagnostico, Consentimiento
from app.models.orden import Orden, Prescripcion, Resultado
from passlib.context import CryptContext

# Contexto de seguridad para el hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_db():
    db = SessionLocal()
    print("🌱 Iniciando sembrado de datos masivo...")

    try:
        # 1. USUARIOS (Sistemas de acceso)
        if db.query(Usuario).count() == 0:
            usuarios = [
                Usuario(username="admin", email="admin@hospital.com", password_hash=pwd_context.hash("admin123"), rol="administracion"),
                Usuario(username="house_md", email="house@hospital.com", password_hash=pwd_context.hash("house123"), rol="profesional"),
                Usuario(username="cajero1", email="caja@hospital.com", password_hash=pwd_context.hash("caja123"), rol="cajero")
            ]
            db.add_all(usuarios)
            print("✅ Usuarios creados: admin, house_md, cajero1")

        # 2. UNIDADES DE ATENCIÓN
        if db.query(UnidadAtencion).count() == 0:
            unidades = [
                UnidadAtencion(nombre="Consultorio 101 - Sede Central", tipo="consultorio", direccion="Av. Libertador #123"),
                UnidadAtencion(nombre="Laboratorio Clínico - Sede Norte", tipo="servicio", direccion="Calle 50 con Av 20"),
                UnidadAtencion(nombre="Unidad de Imágenes - Sede Este", tipo="servicio", direccion="Centro Médico Este")
            ]
            db.add_all(unidades)
            db.commit()
            print("✅ 3 Unidades de atención creadas")
        
        u_cons = db.query(UnidadAtencion).filter(UnidadAtencion.tipo == "consultorio").first()
        u_lab = db.query(UnidadAtencion).filter(UnidadAtencion.nombre.like("%Laboratorio%")).first()

        # 3. PROFESIONALES
        if db.query(Profesional).count() == 0:
            profesionales = [
                Profesional(nombres="Greg", apellidos="House", registro_profesional="RM-12345", categoria="medico", especialidad="Diagnóstico", correo="house@hospital.com", agenda_habilitada=True),
                Profesional(nombres="Lisa", apellidos="Cuddy", registro_profesional="RM-54321", categoria="medico", especialidad="Endocrinología", correo="cuddy@hospital.com", agenda_habilitada=True),
                Profesional(nombres="James", apellidos="Wilson", registro_profesional="RM-98765", categoria="medico", especialidad="Oncología", correo="wilson@hospital.com", agenda_habilitada=True)
            ]
            db.add_all(profesionales)
            db.commit()
            print("✅ 3 Profesionales creados: House, Cuddy, Wilson")

        dr_house = db.query(Profesional).filter(Profesional.registro_profesional == "RM-12345").first()
        dr_cuddy = db.query(Profesional).filter(Profesional.registro_profesional == "RM-54321").first()

        # 4. PACIENTES (PERSONAS)
        if db.query(PersonaAtendida).count() == 0:
            pacientes = [
                PersonaAtendida(tipo_documento="V", numero_documento="20123456", nombres="Pepito", apellidos="Pérez", fecha_nacimiento=datetime(1990, 5, 20), sexo="M", correo="pepito@mail.com"),
                PersonaAtendida(tipo_documento="V", numero_documento="25987654", nombres="María", apellidos="García", fecha_nacimiento=datetime(1995, 8, 12), sexo="F", correo="maria@mail.com"),
                PersonaAtendida(tipo_documento="V", numero_documento="15456789", nombres="Juan", apellidos="Rodríguez", fecha_nacimiento=datetime(1985, 2, 28), sexo="M", correo="juan@mail.com")
            ]
            db.add_all(pacientes)
            db.commit()
            print("✅ 3 Pacientes creados")

        p_pepito = db.query(PersonaAtendida).filter(PersonaAtendida.numero_documento == "20123456").first()
        p_maria = db.query(PersonaAtendida).filter(PersonaAtendida.numero_documento == "25987654").first()

        # 5. AGENDAS (Bloques de tiempo)
        if db.query(Agenda).count() == 0:
            hoy = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
            agendas = [
                # Agenda para House en Consultorio
                Agenda(profesional_id=dr_house.id, unidad_id=u_cons.id, fecha_inicio=hoy, fecha_fin=hoy + timedelta(hours=4), capacidad=5, estado="abierto"),
                # Agenda para Cuddy en Consultorio
                Agenda(profesional_id=dr_cuddy.id, unidad_id=u_cons.id, fecha_inicio=hoy + timedelta(days=1), fecha_fin=hoy + timedelta(days=1, hours=4), capacidad=8, estado="abierto")
            ]
            db.add_all(agendas)
            db.commit()
            print("✅ Agendas creadas para hoy y mañana")

        # 6. CITAS
        if db.query(Cita).count() == 0:
            citas = [
                Cita(persona_id=p_pepito.id, profesional_id=dr_house.id, unidad_id=u_cons.id, fecha_hora_inicio=hoy + timedelta(minutes=30), fecha_hora_fin=hoy + timedelta(minutes=60), motivo="Cefalea constante", estado="confirmada"),
                Cita(persona_id=p_maria.id, profesional_id=dr_house.id, unidad_id=u_cons.id, fecha_hora_inicio=hoy + timedelta(minutes=90), fecha_hora_fin=hoy + timedelta(minutes=120), motivo="Control post-operatorio", estado="confirmada")
            ]
            db.add_all(citas)
            db.commit()
            print("✅ 2 Citas creadas")

        # 7. EPISODIOS CLÍNICOS Y DETALLES
        if db.query(EpisodioAtencion).count() == 0:
            # Episodio 1: Pepito con House
            ep1 = EpisodioAtencion(persona_id=p_pepito.id, motivo="Cefalea intensa migrañosa", tipo="consulta", estado="abierto")
            db.add(ep1)
            db.commit()
            db.refresh(ep1)

            # Nota Clínica y Diagnóstico para ep1
            db.add(NotaClinica(episodio_id=ep1.id, profesional_id=dr_house.id, subjetivo="Dolor punzante", objetivo="Pupilas reactivas", analisis="Migraña clásica", plan="Reposo y medicación"))
            db.add(Diagnostico(episodio_id=ep1.id, codigo="G43.9", descripcion="Migraña no especificada", tipo="definitivo", principal=True))
            
            # Orden de Laboratorio para ep1 (Sección 2.4)
            o1 = Orden(episodio_id=ep1.id, tipo="lab", prioridad="urgente", estado="emitida", detalle=[{"codigo": "HEM-01", "descripcion": "Hemograma", "indicaciones": "Ayuno 8h"}])
            db.add(o1)

            # Episodio 2: María con Cuddy
            ep2 = EpisodioAtencion(persona_id=p_maria.id, motivo="Control tiroideo", tipo="control", estado="abierto")
            db.add(ep2)
            db.commit()
            db.refresh(ep2)

            # Prescripción para ep2 (Sección 2.4)
            p2 = Prescripcion(episodio_id=ep2.id, items=[{"medicamentoCodigo": "LEV-50", "nombre": "Levotiroxina 50mcg", "dosis": "1 tab", "via": "oral", "frecuencia": "diaria", "duracion": "30 días"}])
            db.add(p2)

            db.commit()
            print("✅ Episodios clínicos, notas, diagnósticos y órdenes creadas satisfactoriamente")

    except Exception as e:
        print(f"❌ Error durante el sembrado: {e}")
        db.rollback()
    finally:
        db.close()
        print("🏁 Proceso de sembrado finalizado.")

if __name__ == "__main__":
    seed_db()