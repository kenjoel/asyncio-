from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from starlette.testclient import TestClient
import pytest

from backend.app.database.db import get_db
from backend.app.schema import schema
from main import app

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

client = TestClient(app)


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def get_db_override():
    db = SessionLocal()
    yield db
    db.close()


app.dependency_overrides[get_db] = get_db_override


# def test_get_users():
#     response = client.get("/users")
#     assert response.status_code == 200
#     assert response.json() == {"users": [{"name": "John Doe"}]}


def test_create_user():
    response = client.post("/users/signup",
                           json={"username": "Jose", "email": "Joseph@gmail.com", "password": "password"})
    new_user = schema.User(**response.json())
    assert response.status_code == 201
    assert new_user.email == "Joseph@gmail.com"
