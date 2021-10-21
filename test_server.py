import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base
from api.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

instance_ = {
    "SeriesInstanceUID": "1.2.840.113619.2.410.2807.1589496.16368.1623732908.744",
    "PatientName": "ANO0001",
    "PatientID": "ANO0001",
    "StudyInstanceUID": "1.2.276.0.37.1.354.201605.50651742",
    "InstancesInSeries": 17
}

def test_get_series(test_db):
    response = client.get("/series/")
    assert response.status_code == 200
    assert response.json() == []

def test_post_series_instance(test_db):
    response = client.post(
                url="/series/",
                data=json.dumps(instance_)
            )
    assert response.status_code == 200
    assert response.json() == instance_
