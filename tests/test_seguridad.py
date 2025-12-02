import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

# Credenciales (Deben existir en la BD gracias a seed.py)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
MEDICO_USER = "medico"
MEDICO_PASS = "medico123"

def test_1_login_exitoso():
    """Prueba que el login devuelve un token válido."""
    response = client.post(
        "/auth/login",
        data={"username": ADMIN_USER, "password": ADMIN_PASS},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_2_acceso_denegado_sin_token():
    """Prueba que una ruta protegida rechace el acceso sin token."""
    # Intentamos crear una unidad sin credenciales
    response = client.post("/unidades", json={"nombre": "Test", "tipo": "sede"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_3_acceso_denegado_por_rol():
    """Prueba RBAC: Un 'profesional' NO debe poder crear 'unidades' (Solo Admin)."""
    
    # 1. Nos logueamos como MÉDICO (Rol: profesional)
    login_response = client.post(
        "/auth/login",
        data={"username": MEDICO_USER, "password": MEDICO_PASS},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 2. Intentamos crear una Unidad (Acción reservada para Administradores)
    response = client.post(
        "/unidades",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Unidad Ilegal",
            "tipo": "consultorio"
        }
    )

    # 3. Esperamos un error 403 Forbidden (Prohibido)
    assert response.status_code == 403
    # Verificamos que el mensaje sea el que definimos en dependencies.py
    assert "Requiere rol de Administrador" in response.json()["detail"]