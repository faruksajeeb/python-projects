import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app


# =========================
# TEST DATABASE
# =========================
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# Create tables before tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# =========================
# OVERRIDE DB DEPENDENCY
# =========================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# =========================
# TEST CLIENT FIXTURE
# =========================
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


# =========================
# CLEAN DB BETWEEN TESTS
# =========================
@pytest.fixture(autouse=True)
def clean_db():
    """
    Ensures each test runs with clean database state
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# =========================
# AUTH FIXTURES (IMPORTANT)
# =========================
@pytest.fixture
def auth_token(client):
    # register user
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })

    # login user (IMPORTANT: form-data)
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }