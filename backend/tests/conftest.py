# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import models as models_module
from app.core import auth as auth_module

# -------------------------------------------------------------------
# Test Database: shared in-memory SQLite
# -------------------------------------------------------------------
# StaticPool + "sqlite://" (no /:memory:) ensures all sessions share
# the same in-memory database, so tables persist across connections.
# -------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Use the same Base that models are declared with
Base = models_module.Base

# Create schema once (will be reset per test below)
Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------------
# Dependency overrides
# -------------------------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_create_test_user(db, uid: str = "test-user", name: str = "Test User"):
    user = db.query(models_module.User).filter(models_module.User.id == uid).first()
    if not user:
        user = models_module.User(id=uid, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def override_get_current_user():
    # Always behave as an authenticated test user
    db = TestingSessionLocal()
    try:
        return get_or_create_test_user(db)
    finally:
        db.close()


def override_get_optional_user():
    # For endpoints where auth is optional, still return the test user so
    # tests can easily exercise "logged in" flows.
    db = TestingSessionLocal()
    try:
        return get_or_create_test_user(db)
    finally:
        db.close()


# Wire overrides into the FastAPI app
app.dependency_overrides[auth_module.get_db] = override_get_db
app.dependency_overrides[auth_module.get_current_user] = override_get_current_user
app.dependency_overrides[auth_module.get_optional_user] = override_get_optional_user


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_db():
    """
    Reset the schema before each test.

    Because we're using StaticPool with a shared in-memory DB,
    we explicitly drop & recreate all tables for isolation.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    """
    FastAPI TestClient that uses our overridden dependencies.
    """
    with TestClient(app) as c:
        yield c
