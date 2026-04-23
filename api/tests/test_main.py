import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch("redis.Redis"):
    from main import app

from fastapi.testclient import TestClient

client = TestClient(app)


@patch("main.r")
def test_root_endpoint(mock_redis):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


@patch("main.r")
def test_health_endpoint(mock_redis):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


@patch("main.r")
def test_create_job(mock_redis):
    mock_redis.lpush = MagicMock(return_value=1)
    mock_redis.hset = MagicMock(return_value=1)
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


@patch("main.r")
def test_get_job_status(mock_redis):
    mock_redis.hget = MagicMock(return_value=b"completed")
    response = client.get("/jobs/test-job-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


@patch("main.r")
def test_job_not_found(mock_redis):
    mock_redis.hget = MagicMock(return_value=None)
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404