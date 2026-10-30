"""
NoteGuard AI - Automated Backend API Test Suite
===============================================
Tests:
1. GET / & GET /health
2. POST /api/predict (Multipart image upload)
3. POST /api/predict/camera (Base64 webcam snapshot)
4. GET /api/history & filtering
5. DELETE /api/history/{id}
6. Security checks (invalid file types, corrupt data)
"""

import sys
import base64
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

from app.main import app

def run_tests():
    print("=" * 65)
    print("        NoteGuard AI - Backend API Test Suite Execution        ")
    print("=" * 65)

    with TestClient(app) as client:
        # 1. Root & Health
        print("\n[1] Testing Root & Health Check Endpoints...")
        res_root = client.get("/")
        assert res_root.status_code == 200, f"Root failed: {res_root.text}"
        print(f"    - GET / -> 200 OK: {res_root.json()['project']}")

        res_health = client.get("/health")
        assert res_health.status_code == 200, f"Health check failed: {res_health.text}"
        health_data = res_health.json()
        print(f"    - GET /health -> Status: {health_data['status']} | Models: {health_data['models_loaded']}")
        assert health_data["models_loaded"]["authenticity"] is True, "Authenticity model not loaded!"

        # 2. Image Upload Prediction
        print("\n[2] Testing Image Upload Screening (POST /api/predict)...")
        test_files = list(Path("dataset/test").glob("**/*.jpg"))
        if not test_files:
            test_files = list(Path("../dataset/test").glob("**/*.jpg"))
        sample_file = test_files[0]
        print(f"    - Uploading sample image: {sample_file.name}")

        with open(sample_file, "rb") as f:
            response = client.post(
                "/api/predict",
                files={"file": (sample_file.name, f, "image/jpeg")}
            )

        assert response.status_code == 200, f"Upload prediction failed: {response.text}"
        data = response.json()
        print(f"      * Denomination: {data['denomination'].replace('₹', 'Rs. ')}")
        print(f"      * Authenticity: {data['authenticity']} ({data['confidence']*100:.2f}%)")
        print(f"      * Status Label: {data['status_label']}")
        print(f"      * Blur Sharpness: {data['image_quality']['blur_score']}")
        print(f"      * Brightness: {data['image_quality']['brightness']}")
        print(f"      * Grad-CAM Heatmap URL: {data['gradcam_url']}")
        print(f"      * Inference Latency: {data['inference_time_ms']} ms")
        
        record_id = data["id"]
        assert record_id is not None, "Record ID was not returned!"
        assert data["gradcam_url"] is not None, "Grad-CAM was not generated!"

        # 3. Camera Snapshot Prediction (Base64)
        print("\n[3] Testing Live Camera Screening (POST /api/predict/camera)...")
        with open(sample_file, "rb") as f:
            raw_b64 = base64.b64encode(f.read()).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{raw_b64}"

        cam_response = client.post(
            "/api/predict/camera",
            json={"image_base64": data_url}
        )
        assert cam_response.status_code == 200, f"Camera prediction failed: {cam_response.text}"
        cam_data = cam_response.json()
        print(f"    - Camera Screening Result: {cam_data['denomination'].replace('₹', 'Rs. ')} - {cam_data['authenticity']} ({cam_data['confidence']*100:.2f}%)")

        # 4. History Queries
        print("\n[4] Testing History Endpoints (GET /api/history)...")
        hist_res = client.get("/api/history")
        assert hist_res.status_code == 200, f"History fetch failed: {hist_res.text}"
        hist_data = hist_res.json()
        print(f"    - Total Records in Audit History: {hist_data['total']}")
        assert hist_data["total"] >= 2, "Expected at least 2 saved history entries"

        # Detail view
        detail_res = client.get(f"/api/history/{record_id}")
        assert detail_res.status_code == 200
        print(f"    - GET /api/history/{record_id} -> Successfully retrieved record")

        # 5. Security & Error Handling
        print("\n[5] Testing Security & Validation Error Handling...")
        bad_res = client.post(
            "/api/predict",
            files={"file": ("test.txt", b"plain text is not an image", "text/plain")}
        )
        assert bad_res.status_code in [400, 415], f"Expected 400/415 for text file, got {bad_res.status_code}"
        print(f"    - Text file upload safely rejected with HTTP {bad_res.status_code}")

        empty_res = client.post("/api/predict", files={"file": ("empty.jpg", b"", "image/jpeg")})
        assert empty_res.status_code in [400, 422], f"Expected 400/422 for empty file, got {empty_res.status_code}"
        print(f"    - Empty file safely rejected with HTTP {empty_res.status_code}")

        # 6. History Deletion
        print("\n[6] Testing Record Deletion (DELETE /api/history/{id})...")
        del_res = client.delete(f"/api/history/{record_id}")
        assert del_res.status_code == 200
        print(f"    - Record #{record_id} successfully deleted from SQLite audit ledger")

    print("\n" + "=" * 65)
    print("All NoteGuard AI Backend API Tests Passed Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
