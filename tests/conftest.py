import pytest
import sys
from pathlib import Path

# Make project importable when tests run from repo root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app as flask_app  # imports the Flask app instance:contentReference[oaicite:4]{index=4}

@pytest.fixture()
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test_secret",
    )
    yield flask_app

@pytest.fixture()
def client(app):
    return app.test_client()
