from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_admin_token():
    login = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    return login.json()["access_token"]

def test_crud_flujo_completo_entidades():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Test Unidades
    unidad_res = client.post("/unidades", headers=headers, json={
        "nombre": "Sede Norte", "tipo": "sede", "direccion": "Calle 1", "telefono": "123"
    })
    assert unidad_res.status_code == 201
    unidad_id = unidad_res.json()["id"]

    # 2. Test Profesionales (Duplicado)
    prof_data = {
        "nombres": "Ana", "apellidos": "Sosa", "registro_profesional": "REG-101",
        "categoria": "medico", "especialidad": "General"
    }
    client.post("/profesionales", headers=headers, json=prof_data)
    prof_duplicado = client.post("/profesionales", headers=headers, json=prof_data)
    assert prof_duplicado.status_code == 409 # Conflicto por registro existente

    # 3. Test Personas (Eliminación Lógica)
    persona_res = client.post("/personas", headers=headers, json={
        "tipo_documento": "V", "numero_documento": "12345678",
        "nombres": "Juan", "apellidos": "Doe", "fecha_nacimiento": "1995-01-01", "sexo": "M"
    })
    persona_id = persona_res.json()["id"]
    client.delete(f"/personas/{persona_id}", headers=headers)
    
    get_res = client.get(f"/personas/{persona_id}", headers=headers)
    assert get_res.json()["estado"] == "inactivo"