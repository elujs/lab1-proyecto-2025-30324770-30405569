import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    # Asegúrate de ejecutar seed.py antes para que este usuario exista
    res = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    return res.json()["access_token"]

def test_flujo_clinico_completo():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    ts = int(time.time()) # Sufijo único para datos

    # 1. CREACIÓN DE IDENTIDADES (2.1)
    # Paciente
    p_res = client.post("/personas", headers=headers, json={
        "tipo_documento": "V", "numero_documento": f"DOC-{ts}",
        "nombres": "Test", "apellidos": "Paciente", "fecha_nacimiento": "1990-05-20", "sexo": "M"
    })
    assert p_res.status_code == 201, f"Error Paciente: {p_res.json()}"
    p_id = p_res.json()["id"]

    # Profesional
    dr_res = client.post("/profesionales", headers=headers, json={
        "nombres": "Dr", "apellidos": "Test", "registro_profesional": f"REG-{ts}",
        "categoria": "medico", "especialidad": "General"
    })
    assert dr_res.status_code == 201, f"Error Profesional: {dr_res.json()}"
    dr_id = dr_res.json()["id"]

    # Unidad
    u_res = client.post("/unidades", headers=headers, json={"nombre": f"Sede-{ts}", "tipo": "sede"})
    assert u_res.status_code == 201, f"Error Unidad: {u_res.json()}"
    u_id = u_res.json()["id"]

    # 2. DISPONIBILIDAD Y CITAS (2.2)
    # Bloque de Agenda
    ag_res = client.post("/agenda", headers=headers, json={
        "profesional_id": dr_id, "unidad_id": u_id,
        "fecha_inicio": "2026-10-10T08:00:00", "fecha_fin": "2026-10-10T12:00:00", "capacidad": 1
    })
    assert ag_res.status_code == 201, f"Error Agenda: {ag_res.json()}"

    # Crear Cita
    cita_res = client.post("/citas", headers=headers, json={
        "persona_id": p_id, "profesional_id": dr_id, "unidad_id": u_id,
        "fecha_hora_inicio": "2026-10-10T09:00:00", "fecha_hora_fin": "2026-10-10T09:30:00",
        "motivo": "Control anual"
    })
    assert cita_res.status_code == 201, f"Error Cita: {cita_res.json()}"

    # Verificar Solapamiento (Debe dar 409)
    cita_fail = client.post("/citas", headers=headers, json={
        "persona_id": p_id, "profesional_id": dr_id, "unidad_id": u_id,
        "fecha_hora_inicio": "2026-10-10T09:15:00", "fecha_hora_fin": "2026-10-10T09:45:00"
    })
    assert cita_fail.status_code == 409, "Debió fallar por solapamiento"

    # 3. REGISTRO CLÍNICO (2.3)
    # Abrir Episodio
    epi_res = client.post("/episodios", headers=headers, json={
        "persona_id": p_id, "motivo": "Dolor lumbar", "tipo": "consulta"
    })
    assert epi_res.status_code == 201, f"Error Episodio: {epi_res.json()}"
    e_id = epi_res.json()["id"]

    # Nota Clínica
    nota_res = client.post(f"/episodios/{e_id}/notas", headers=headers, json={
        "profesional_id": dr_id, "subjetivo": "Dolor", "objetivo": "Normal", "analisis": "Normal", "plan": "Descanso"
    })
    assert nota_res.status_code == 200, f"Error Nota: {nota_res.json()}"

    # Diagnóstico Principal Único (Verificar restricción)
    client.post(f"/episodios/{e_id}/diagnosticos", headers=headers, json={
        "codigo": "M54.5", "descripcion": "Lumbago", "tipo": "presuntivo", "principal": True
    })
    diag_fail = client.post(f"/episodios/{e_id}/diagnosticos", headers=headers, json={
        "codigo": "Z00.0", "descripcion": "Examen", "tipo": "presuntivo", "principal": True
    })
    assert diag_fail.status_code == 409, "Debió fallar: ya hay un diagnóstico principal"

    print("\n✅ ¡Todas las verificaciones de las Secciones 2.1 a 2.3 pasaron con éxito!")

## se ejecuta con python -m pytest tests/test_completo.py -s