import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.base import Base
from app.main import app
from app.api.v1.students import get_db as get_db_students
from app.api.v1.invoices import get_db as get_db_invoices
from app.api.v1.schools import get_db as get_db_schools


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db_students] = override_get_db
    app.dependency_overrides[get_db_invoices] = override_get_db
    app.dependency_overrides[get_db_schools] = override_get_db

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def school(client):
    payload = {
        "name": "Test School",
        "tax_id": str(uuid.uuid4()),
        "address": "Fake Street 123",
        "is_active": True,
    }
    resp = client.post("/api/v1/schools/", json=payload)
    assert resp.status_code == 201
    return resp.json()
