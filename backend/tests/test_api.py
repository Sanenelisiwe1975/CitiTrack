"""API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_create_report():
    """Test report creation"""
    report_data = {
        "category": "pothole",
        "description": "Large pothole on Main Street",
        "location": {
            "latitude": -26.2041,
            "longitude": 28.0473,
            "address": "Main Street, Johannesburg"
        },
        "language": "en"
    }
    
    response = client.post("/api/reports", json=report_data)
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_reports():
    """Test getting all reports"""
    response = client.get("/api/reports")
    assert response.status_code == 200
    assert "reports" in response.json()


def test_dashboard_stats():
    """Test dashboard statistics"""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    assert "summary" in response.json()