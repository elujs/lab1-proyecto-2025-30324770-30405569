from app.database import SessionLocal, engine, Base
from app.models.usuario import Usuario
from app.models.persona import PersonaAtendida
from app.models.profesional import Profesional
from app.models.unidad import UnidadAtencion
from app.models.agenda import Agenda
from app.models.cita import Cita
from app.models.episodio import EpisodioAtencion
from app.models.clinico import NotaClinica, Diagnostico, Consentimiento
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Inicializar contexto de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_db():
    db = SessionLocal()
    print("🌱 Iniciando sembrado de datos...")

    # 1. USUARIOS
    if not db.query(Usuario).filter(Usuario.username == "admin").first():
        admin = Usuario(
            username="admin", 
            email="admin@hospital.com", 
            password_hash=pwd_context.hash("admin123"), 
            rol="administracion"
        )
        db.add(admin)
        print("✅ Usuario Admin creado")

    if not db.query(Usuario).filter(Usuario.username == "medico").first():
        medico_user = Usuario(
            username="medico", 
            email="medico@hospital.com", 
            password_hash=pwd_context.hash("medico123"), 
            rol="profesional" # Rol limitado (no es admin)
        )
        db.add(medico_user)
        db.commit()
        print("✅ Usuario Médico creado (user: medico / pass: medico123)")

    # 2. UNIDAD DE ATENCIÓN
    unidad = db.query(UnidadAtencion).first()
    if not unidad:
        unidad = UnidadAtencion(
            nombre="Sede Central - Consultorio 101",
            tipo="consultorio",
            direccion="Av. Libertador #123",
            horario_referencia="8:00 - 17:00"
        )
        db.add(unidad)
        db.commit() 
        db.refresh(unidad)
        print("✅ Unidad creada")

    # 3. PROFESIONAL
    if db.query(Profesional).count() == 0:
        profe_house = Profesional(
            nombres="Greg", apellidos="House",
            registro_profesional="RM-12345",
            categoria="medico",
            especialidad="Diagnóstico",
            correo="house@hospital.com",
            agenda_habilitada=True
        )
        profe_cuddy = Profesional(
            nombres="Lisa", apellidos="Cuddy",
            registro_profesional="RM-54321",
            categoria="medico",
            especialidad="Medicina Interna",
            correo="cuddy@hospital.com",
            agenda_habilitada=True
        )
        db.add_all([profe_house, profe_cuddy]) 
        db.commit() 
        
        #Este profesional se usara en la agenda
        profe = profe_house 
        print("✅ 2 Profesionales creados (House y Cuddy)")
    else:
        # Si ya existen, obtenemos uno para continuar la secuencia
        profe = db.query(Profesional).filter(Profesional.registro_profesional == "RM-12345").first()

    # 4. PACIENTE (PERSONA)
    paciente = db.query(PersonaAtendida).first()
    if not paciente:
        paciente = PersonaAtendida(
            tipo_documento="CC", numero_documento="99887766",
            nombres="Pepito", apellidos="Pérez",
            fecha_nacimiento=datetime(1990, 5, 20),
            sexo="M", correo="pepito@mail.com", telefono="555-0000"
        )
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        print("✅ Paciente creado")

    # 5. AGENDA (Bloque disponible para HOY)
    agenda = db.query(Agenda).first()
    inicio_agenda = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    fin_agenda = inicio_agenda + timedelta(hours=4)
    
    if not agenda:
        agenda = Agenda(
            profesional_id=profe.id,
            unidad_id=unidad.id,
            fecha_inicio=inicio_agenda,
            fecha_fin=fin_agenda,
            capacidad=10,
            estado="abierto"
        )
        db.add(agenda)
        db.commit()
        db.refresh(agenda)
        print("✅ Agenda creada (8:00 AM - 12:00 PM)")

    # 6. CITA
    cita = db.query(Cita).first()
    if not cita:
        cita = Cita(
            persona_id=paciente.id,
            profesional_id=profe.id,
            unidad_id=unidad.id,
            fecha_hora_inicio=inicio_agenda, # Cita a las 8:00
            fecha_hora_fin=inicio_agenda + timedelta(minutes=30),
            motivo="Dolor de cabeza recurrente",
            estado="confirmada"
        )
        db.add(cita)
        db.commit()
        print("✅ Cita creada")

    # 7. EPISODIO CLÍNICO
    episodio = db.query(EpisodioAtencion).first()
    if not episodio:
        episodio = EpisodioAtencion(
            persona_id=paciente.id,
            motivo="Paciente refiere cefalea intensa",
            tipo="consulta",
            estado="abierto"
        )
        db.add(episodio)
        db.commit()
        db.refresh(episodio)
        print("✅ Episodio clínico abierto")

        # 7.1 NOTA CLÍNICA
        nota = NotaClinica(
            episodio_id=episodio.id,
            profesional_id=profe.id,
            subjetivo="Paciente de 34 años...",
            objetivo="TA 120/80, FC 70...",
            analisis="Posible migraña tensional",
            plan="Paracetamol 1g cada 8h"
        )
        db.add(nota)
        
        # 7.2 DIAGNÓSTICO
        diag = Diagnostico(
            episodio_id=episodio.id,
            codigo="G44.2",
            descripcion="Cefalea tensional",
            tipo="presuntivo",
            principal=True
        )
        db.add(diag)

        # 7.3 CONSENTIMIENTO 
        consent = Consentimiento(
            persona_id=paciente.id,
            episodio_id=episodio.id,
            tipo_procedimiento="Toma de biopsia",
            metodo="firma_digital",
            archivo_id="doc_firmado_base64_xyz"
        )
        db.add(consent)
        
        db.commit()
        print("✅ Detalles clínicos agregados (Nota, Diagnostico, Consentimiento)")

    db.close()
    print("🏁 ¡Sembrado de datos completado con éxito!")

if __name__ == "__main__":
    seed_db()