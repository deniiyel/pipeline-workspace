import pytest
from fastapi.testclient import TestClient
from main import app, metrics_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_metrics_store():
    metrics_db.clear()

def test_record_metric():
    res = client.post("/metrics", json={"metric_name": "cpu_usage", "value": 45.5})
    assert res.status_code == 201
    assert res.json()["metric_name"] == "cpu_usage"

def test_get_metric_stats_success():
    client.post("/metrics", json={"metric_name": "cpu_usage", "value": 10.0})
    client.post("/metrics", json={"metric_name": "cpu_usage", "value": 20.0})
    client.post("/metrics", json={"metric_name": "cpu_usage", "value": 30.0})

    res = client.get("/metrics/cpu_usage/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 3
    assert data["min_value"] == 10.0
    assert data["max_value"] == 30.0
    assert data["avg_value"] == 20.0

def test_get_metric_stats_not_found():
    res = client.get("/metrics/non_existent/stats")
    assert res.status_code == 404

def test_record_empty_metric_name():
    res = client.post("/metrics", json={"metric_name": "   ", "value": 50.0})
    assert res.status_code == 400

def test_clear_metrics():
    client.post("/metrics", json={"metric_name": "memory_usage", "value": 512.0})
    client.delete("/metrics")
    res = client.get("/metrics/memory_usage/stats")
    assert res.status_code == 404