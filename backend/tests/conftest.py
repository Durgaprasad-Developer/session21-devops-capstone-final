"""
conftest.py — shared pytest fixtures.

Uses an in-memory SQLite database so tests are fully isolated from the
production PostgreSQL instance.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# SQLite in-memory for isolation
TEST_DB_URL = "sqlite:///./test_bookease.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables before the test session and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clear_tables():
    """Truncate all data between tests for isolation."""
    yield
    from app import models
    db = TestingSessionLocal()
    try:
        db.query(models.Appointment).delete()
        db.query(models.Patient).delete()
        db.query(models.Doctor).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Helper fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_doctor(client):
    resp = client.post(
        "/api/doctors",
        json={
            "name": "Dr. Test",
            "speciality": "General",
            "email": "test.doc@example.com",
            "availability_start": "09:00:00",
            "availability_end": "17:00:00",
        },
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def sample_patient(client):
    resp = client.post(
        "/api/patients",
        json={"name": "Test Patient", "email": "test.patient@example.com"},
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def sample_appointment(client, sample_doctor, sample_patient):
    resp = client.post(
        "/api/appointments",
        json={
            "doctor_id": sample_doctor["id"],
            "patient_id": sample_patient["id"],
            "appointment_date": "2030-01-15",
            "start_time": "10:00:00",
            "end_time": "10:30:00",
            "reason": "Check-up",
        },
    )
    assert resp.status_code == 201
    return resp.json()
