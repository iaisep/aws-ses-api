"""
Pruebas para la API de AWS SES
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Prueba el endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "timestamp" in data

def test_health_endpoint():
    """Prueba el endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "aws-ses-api"
    assert "timestamp" in data

def test_send_email_missing_credentials():
    """Prueba envío de email sin credenciales"""
    email_data = {
        "credentials": {
            "access_key": "",
            "secret_key": "",
            "region": "us-east-1"
        },
        "from_email": "test@example.com",
        "destination": {
            "to_addresses": ["recipient@example.com"]
        },
        "content": {
            "subject": "Test Subject",
            "text_body": "Test message"
        }
    }
    
    response = client.post("/send-email", json=email_data)
    assert response.status_code == 401

def test_send_email_invalid_email():
    """Prueba envío con email inválido"""
    email_data = {
        "credentials": {
            "access_key": "fake_key",
            "secret_key": "fake_secret",
            "region": "us-east-1"
        },
        "from_email": "invalid-email",
        "destination": {
            "to_addresses": ["recipient@example.com"]
        },
        "content": {
            "subject": "Test Subject",
            "text_body": "Test message"
        }
    }
    
    response = client.post("/send-email", json=email_data)
    assert response.status_code == 422  # Validation error

def test_send_simple_email_missing_params():
    """Prueba el endpoint simple sin parámetros"""
    response = client.post("/send-simple-email")
    assert response.status_code == 422  # Missing required parameters

# Nota: Para pruebas reales con AWS, necesitarías credenciales válidas
# y configurar un entorno de testing separado