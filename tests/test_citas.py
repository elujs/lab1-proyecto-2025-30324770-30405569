from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def get_auth_headers():
    login = client.post("/auth/login", data={"username": ADMIN_USER, "password": ADMIN_PASS})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_crear_cita_sin_agenda_falla():
    """
    Prueba Crítica: Intentar crear una cita en una fecha donde NO existe agenda abierta.
    Debe fallar con 400 Bad Request.
    """
    headers = get_auth_headers()
    
    # 1. Usamos una fecha futura donde seguro no hay agenda creada por el seed
    fecha_futura = datetime.now() + timedelta(days=300)


    # Hacemos un GET para obtener un profesional y unidad cualquiera
    profe = client.get("/profesionales", headers=headers).json()[0]
    unidad = client.get("/unidades", headers=headers).json()[0]
    paciente = client.get("/personas", headers=headers).json()[0]

    cita_payload = {
        "persona_id": paciente["id"],
        "profesional_id": profe["id"],
        "unidad_id": unidad["id"],
        "fecha_hora_inicio": fecha_futura.isoformat(),
        "fecha_hora_fin": (fecha_futura + timedelta(minutes=30)).isoformat(),
        "motivo": "Intento de cita ilegal",
        "canal": "presencial"
    }

    # 2. Intentamos crear la cita
    response = client.post("/citas", json=cita_payload, headers=headers)

    # 3. Verificación
    assert response.status_code == 400
    assert "No hay agenda disponible" in response.json()["detail"]