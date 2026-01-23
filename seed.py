import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Asegurar que Python encuentre la carpeta 'app'
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
from app.models.cobertura import Aseguradora, PlanCobertura, Afiliacion
from app.models.facturacion import Prestacion, Arancel, Factura, FacturaItem, Pago
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_db():
    print("🛠️  Garantizando estructura de tablas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    print("🌱 Iniciando sembrado masivo de datos (Secciones 2.1 a 2.7)...")

    try:
        # 1. USUARIOS
        if db.query(Usuario).count() == 0:
            db.add_all([
                Usuario(username="admin", email="admin@hospital.com", password_hash=pwd_context.hash("admin123"), rol="administracion"),
                Usuario(username="medico", email="medico@hospital.com", password_hash=pwd_context.hash("medico123"), rol="profesional"),
                Usuario(username="cajero", email="caja@hospital.com", password_hash=pwd_context.hash("caja123"), rol="cajero")
            ])
            db.commit()
            print("✅ Usuarios creados (admin, medico, cajero)")

        # 2. INFRAESTRUCTURA (UNIDADES)
        if db.query(UnidadAtencion).count() == 0:
            db.add_all([
                UnidadAtencion(nombre="Consultorio 101 - Sede Central", tipo="consultorio", direccion="Av. Libertador #123"),
                UnidadAtencion(nombre="Laboratorio Clínico", tipo="servicio", direccion="Piso 2"),
                UnidadAtencion(nombre="Sede Norte - Urgencias", tipo="sede", direccion="Calle 50")
            ])
            db.commit()
            print("✅ Unidades de atención creadas")
        u_cons = db.query(UnidadAtencion).filter(UnidadAtencion.tipo == "consultorio").first()

        # 3. PROFESIONALES
        if db.query(Profesional).count() == 0:
            db.add_all([
                Profesional(nombres="Greg", apellidos="House", registro_profesional="RM-12345", categoria="medico", especialidad="Diagnóstico", correo="house@hospital.com"),
                Profesional(nombres="Lisa", apellidos="Cuddy", registro_profesional="RM-54321", categoria="medico", especialidad="Endocrinología", correo="cuddy@hospital.com")
            ])
            db.commit()
            print("✅ Médicos creados (House y Cuddy)")
        dr_house = db.query(Profesional).filter(Profesional.registro_profesional == "RM-12345").first()

        # 4. PACIENTES
        if db.query(PersonaAtendida).count() == 0:
            db.add_all([
                PersonaAtendida(tipo_documento="V", numero_documento="20123456", nombres="Pepito", apellidos="Pérez", fecha_nacimiento=datetime(1990, 5, 20), sexo="M", correo="pepito@mail.com"),
                PersonaAtendida(tipo_documento="V", numero_documento="25987654", nombres="María", apellidos="García", fecha_nacimiento=datetime(1995, 8, 12), sexo="F", correo="maria@mail.com")
            ])
            db.commit()
            print("✅ Pacientes creados")
        p_pepito = db.query(PersonaAtendida).filter(PersonaAtendida.numero_documento == "20123456").first()

        # 5. COBERTURA (ASEGURADORAS Y PLANES)
        if db.query(Aseguradora).count() == 0:
            aseg = Aseguradora(nombre="Salud Total", nit="900.123.456-1", contacto="0800-SALUD")
            db.add(aseg)
            db.commit()
            plan = PlanCobertura(aseguradora_id=aseg.id, nombre="Plan Platino", condiciones_generales="Cobertura 100% en urgencias")
            db.add(plan)
            db.commit()
            # Afiliamos a Pepito
            db.add(Afiliacion(persona_id=p_pepito.id, plan_id=plan.id, numero_poliza="POL-999", vigente_desde=datetime.now().date(), vigente_hasta=datetime(2030,1,1).date()))
            print("✅ Cobertura y Afiliación configurada")
        plan_ref = db.query(PlanCobertura).first()

        # 6. CATÁLOGO (PRESTACIONES Y ARANCELES)
        if db.query(Prestacion).count() == 0:
            cons = Prestacion(codigo="MED-01", nombre="Consulta Medicina General", grupo="Consultas")
            lab = Prestacion(codigo="LAB-01", nombre="Hemograma Completo", grupo="Laboratorio")
            db.add_all([cons, lab])
            db.commit()
            # Aranceles
            db.add(Arancel(prestacion_codigo="MED-01", plan_id=plan_ref.id, valor_base=Decimal("50.00"), vigente_desde=datetime.now().date()))
            db.add(Arancel(prestacion_codigo="LAB-01", plan_id=plan_ref.id, valor_base=Decimal("15.00"), vigente_desde=datetime.now().date()))
            print("✅ Catálogo de prestaciones y aranceles creado")

        # 7. AGENDAS Y CITAS
        if db.query(Agenda).count() == 0:
            hoy = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
            ag = Agenda(profesional_id=dr_house.id, unidad_id=u_cons.id, fecha_inicio=hoy, fecha_fin=hoy + timedelta(hours=4), capacidad=5)
            db.add(ag)
            db.commit()
            db.add(Cita(persona_id=p_pepito.id, profesional_id=dr_house.id, unidad_id=u_cons.id, fecha_hora_inicio=hoy+timedelta(minutes=30), fecha_hora_fin=hoy+timedelta(minutes=60), motivo="Control Anual", estado="confirmada"))
            print("✅ Agenda y Cita creada")

        # 8. REGISTRO CLÍNICO, ÓRDENES Y FACTURACIÓN
        if db.query(EpisodioAtencion).count() == 0:
            epi = EpisodioAtencion(persona_id=p_pepito.id, motivo="Cefalea migrañosa", tipo="consulta")
            db.add(epi)
            db.commit()
            db.refresh(epi)
            
            # Detalle clínico
            db.add(NotaClinica(episodio_id=epi.id, profesional_id=dr_house.id, subjetivo="Dolor fuerte", objetivo="TA normal", analisis="Migraña", plan="Reposo"))
            db.add(Diagnostico(episodio_id=epi.id, codigo="G43.9", descripcion="Migraña", tipo="definitivo", principal=True))
            
            # Órdenes
            ord1 = Orden(episodio_id=epi.id, tipo="lab", prioridad="normal", estado="completada", detalle=[{"codigo": "LAB-01", "descripcion": "Hemograma", "indicaciones": "Ayuno"}])
            db.add(ord1)
            db.commit()
            db.refresh(ord1)
            db.add(Resultado(orden_id=ord1.id, resumen="Valores normales", version=1))
            
            # Facturación (Sección 2.7)
            fact = Factura(numero="FAC-000001", persona_id=p_pepito.id, total=Decimal("65.00"), estado="emitida")
            db.add(fact)
            db.commit()
            db.refresh(fact)
            db.add(FacturaItem(factura_id=fact.id, prestacion_codigo="MED-01", cantidad=1, valor_unitario=Decimal("50.00"), total_linea=Decimal("50.00")))
            db.add(FacturaItem(factura_id=fact.id, prestacion_codigo="LAB-01", cantidad=1, valor_unitario=Decimal("15.00"), total_linea=Decimal("15.00")))
            # Pago parcial
            db.add(Pago(factura_id=fact.id, monto=Decimal("65.00"), medio="efectivo", referencia="PAGO-SEED"))
            fact.estado = "pagada"
            print("✅ Episodio clínico, órdenes, factura y pago creados satisfactoriamente")

        db.commit()
    except Exception as e:
        print(f"❌ Error durante el sembrado: {e}")
        db.rollback()
    finally:
        db.close()
        print("🏁 Proceso de sembrado finalizado.")

if __name__ == "__main__":
    seed_db()