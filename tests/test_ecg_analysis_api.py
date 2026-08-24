from fastapi.testclient import TestClient
from pathlib import Path
from ecg_analyzer.api import app
from ecg_analyzer.io import load_ecg_file

client = TestClient(app)

test_path = Path.cwd()


def test_analyze_ecg_record_success():
    payload = load_ecg_file(test_path, "04048_hr", "500").model_dump()
    response = client.post("/ecg/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    print(body)


if __name__ == "__main__":
    test_analyze_ecg_record_success()
