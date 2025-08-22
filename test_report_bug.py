from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # ✅ This line creates the client

def test_report_bug_missing_title():

    payload = {
        # "title" is missing
        "description": "No title provided",
        "severity": "low"
    }
    response = client.post("/api/v1/report-bug", json=payload)
    print("RESPONSE JSON:", response.json())
    assert response.status_code == 422
    assert "detail" in response.json()