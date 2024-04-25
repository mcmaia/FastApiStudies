from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi import status
import pytest

from ..routers.todos import get_db, get_current_user
from ..database import Base
from ..main import app
from ..models import Todos

import os
from dotenv import load_dotenv

load_dotenv()

PSQL_PASSWORD=os.getenv("PSQL_PASSWORD")
HOST=os.getenv("HOST")
STAGING_DATABASE=os.getenv("STAGING_DATABASE")


SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{PSQL_PASSWORD}@{HOST}:5432/{STAGING_DATABASE}'
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool
    )


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'john_doe', 'id': 1, 'user_role': 'Admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Go to sleep",
        description="Need to rest",
        priority=5,
        complete=False,
        owner_id=4
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []