import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_stats_endpoint():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_queries" in data
    assert "success_rate" in data
    assert "avg_latency_ms" in data

def test_history_endpoint():
    response = client.get("/api/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_generate_empty_question():
    response = client.post("/api/generate", json={
        "question": "",
        "schema": "CREATE TABLE test (id INT);",
        "db_name": "Custom"
    })
    assert response.status_code == 400

def test_generate_valid_question():
    response = client.post("/api/generate", json={
        "question": "How many employees are there?",
        "schema": "CREATE TABLE employees (emp_id INT, name TEXT, department TEXT, salary REAL);",
        "db_name": "HR Database"
    })
    assert response.status_code == 200
    data = response.json()
    assert "sql" in data
    assert "latency_ms" in data
    assert "execution" in data
    assert len(data["sql"]) > 0

if __name__ == "__main__":
    print("Running tests...")
    test_root()
    print("✅ test_root passed")
    test_stats_endpoint()
    print("✅ test_stats_endpoint passed")
    test_history_endpoint()
    print("✅ test_history_endpoint passed")
    test_generate_empty_question()
    print("✅ test_generate_empty_question passed")
    test_generate_valid_question()
    print("✅ test_generate_valid_question passed")
    print("\nAll tests passed!")