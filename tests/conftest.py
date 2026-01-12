import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.base import Base
from app.main import app
from app.api.v1.students import get_db as get_db_students
from app.api.v1.invoices import get_db as get_db_invoices


# Use a separate SQLite database for tests
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
    # Recreate all tables for the test session
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Override DB dependencies in routers
    app.dependency_overrides[get_db_students] = override_get_db
    app.dependency_overrides[get_db_invoices] = override_get_db

    yield

    # Clean up after test session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)
