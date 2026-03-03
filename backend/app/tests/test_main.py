import os
import sys

# Fake Daten
os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_password"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["SECRET_KEY"] = "super-geheimes-test-passwort"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_mathe():
    assert 1 + 1 == 2

def test_api_existiert():
    """Prüft, ob die FastAPI App geladen werden kann und antwortet."""
    response = client.get("/openapi.json")
    assert response.status_code == 200