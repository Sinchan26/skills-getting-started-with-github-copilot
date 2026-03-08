"""
Pytest configuration and shared fixtures
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI app.
    Each test gets a fresh TestClient instance.
    """
    return TestClient(app)
