
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Celestius Registration API is running"


def test_create_registration(client):
    response = client.post(
        "/register",
        json={
            "name": "Test Participant",
            "email": "test@example.com",
            "college": "CIT",
            "department": "CSBS",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Participant"
    assert data["email"] == "test@example.com"
    assert data["id"] == 1


def test_duplicate_email(client):
    payload = {
        "name": "Test Participant",
        "email": "duplicate@example.com",
        "college": "CIT",
        "department": "CSBS",
    }

    first_response = client.post("/register", json=payload)
    second_response = client.post("/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "This email is already registered."


def test_invalid_email(client):
    response = client.post(
        "/register",
        json={
            "name": "Test Participant",
            "email": "not-an-email",
            "college": "CIT",
            "department": "CSBS",
        },
    )

    assert response.status_code == 422


def test_list_registrations(client):
    client.post(
        "/register",
        json={
            "name": "First Participant",
            "email": "first@example.com",
        },
    )
    client.post(
        "/register",
        json={
            "name": "Second Participant",
            "email": "second@example.com",
        },
    )

    response = client.get("/registrations")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "first@example.com"


def test_registration_not_found(client):
    response = client.get("/registrations/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Registration not found."

def test_event_capacity(client):
    for i in range(50):
        response = client.post(
            "/register",
            json={
                "name": f"Participant {i + 1}",
                "email": f"participant{i + 1}@example.com",
            },
        )
        assert response.status_code == 201

    response = client.post(
        "/register",
        json={
            "name": "Participant 51",
            "email": "participant51@example.com",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Event registration is full."
