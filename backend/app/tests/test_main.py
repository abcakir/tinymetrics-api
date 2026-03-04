import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

# 1. Fake-Umgebungsvariablen
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "test"
os.environ["SECRET_KEY"] = "super-secret"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.api.deps import get_db
from app.db.base import Base

# --- 4. TEST-DATENBANK SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Erstelle alle Tabellen in der leeren Test-Datenbank
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Echte Datenbank durch Test-Datenbank ersetzen
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Tests

def test_user_registrierung():
    """Testet, ob sich ein neuer Nutzer registrieren kann."""

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "MeinGeheimesPasswort123"}
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_user_login():
    """Testet, ob sich ein User einloggen und einen Token holen kann."""
    
    client.post(
        "/api/v1/auth/register",
        json={"email": "login_test@example.com", "password": "SuperSecretPassword1!"}
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login_test@example.com", 
            "password": "SuperSecretPassword1!"
        }
    )

    assert response.status_code == 200

    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_create_and_redirect_url():
    """Testet das Kürzen einer URL und die anschließende Weiterleitung."""
    
    client.post(
        "/api/v1/auth/register",
        json={"email": "url_tester@example.com", "password": "SuperSecretPassword1!"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "url_tester@example.com", "password": "SuperSecretPassword1!"}
    )
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/urls", 
        json={"original_url": "https://www.pytest.org"},
        headers=headers
    )
    
    assert create_response.status_code in [200, 201] 
    
    url_data = create_response.json()
    assert "short_code" in url_data
    short_code = url_data["short_code"]

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False 
    )
    
    # 307 Temporary Redirect (oder 302/308, je nach deiner main.py)
    assert redirect_response.status_code in [302, 307, 308]

    assert redirect_response.headers["location"] == "https://www.pytest.org/"