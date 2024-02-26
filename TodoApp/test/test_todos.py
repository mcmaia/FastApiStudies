from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi import status

from ..routers.todos import get_db, get_current_user
from ..database import Base
from ..main import app

import os
from dotenv import load_dotenv

load_dotenv()

PSQL_PASSWORD=os.getenv("PSQL_PASSWORD")
HOST=os.getenv("HOST")
# DATABASE=os.getenv("DATABASE")


SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{PSQL_PASSWORD}@{HOST}:5432/TestTodoAppDatabase'
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

def test_read_all_authenticated():
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK