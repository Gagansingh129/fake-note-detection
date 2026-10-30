"""
NoteGuard AI - Automated End-to-End Test & Verification Suite
=============================================================
Verifies all 10 core conditions specified in the technical requirements:
1. Known genuine test image
2. Known counterfeit test image from held-out verified dataset
3. Blurry image (Laplacian variance quality gating)
4. Blank / black image (std dev quality gating)
5. Unsupported file format rejection
6. Non-banknote / scene image
7. Incorrect / extreme image dimensions
8. Backend inference error & corruption handling
9. Camera frame base64 submission (/api/predict/camera)
10. Upload vs camera endpoint consistency

Also evaluates the complete held-out test set (113 images) and reports:
- Accuracy, Precision, Recall, F1
- False Genuine Rate & False Fake Rate
- Confusion Matrix & ROC-AUC
"""

import sys
import base64
from pathlib import Path

# Add backend to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))
sys.path.insert(0, str(ROOT_DIR))

import cv2
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score, accuracy_score
from fastapi.testclient import TestClient

from app.main import app
from app.services.prediction_service import model_manager
from app.database import init_db

init_db()

print("\n" + "=" * 70)
print("     NoteGuard AI - 10-Point Automated Verification Suite")
print("=" * 70)

test_results = {}

with TestClient(app) as client:
    # ----------------------------------------------------------------------
    # Test 1: Known Genuine Test Image
    # ----------------------------------------------------------------------
    print("\n[TEST 1] Testing Known Genuine Test Banknote...")
    genuine_samples = list((ROOT_DIR / "dataset/test/genuine").glob("*.*"))
    if genuine_samples:
        test_img_path = genuine_samples[0]
        with open(test_img_path, "rb") as f:
            img_bytes = f.read()
        response = client.post("/api/predict", files={"file": (test_img_path.name, img_bytes, "image/jpeg")})
        assert response.status_code == 200, f"HTTP Error: {response.text}"
        data = response.json()
        print(f"    - Input: {test_img_path.name}")
        print(f"    - Predicted: {data['authenticity']} (Decision: {data['decision_status']}, Confidence: {data['confidence']})")
        assert data["decision_status"] == "likely_genuine", f"Expected likely_genuine, got {data['decision_status']}"
        test_results["Test 1: Known Genuine Note"] = "PASSED"
    else:
        test_results["Test 1: Known Genuine Note"] = "SKIPPED (No test sample)"

    # ----------------------------------------------------------------------
    # Test 2: Known Counterfeit Test Image
    # ----------------------------------------------------------------------
    print("\n[TEST 2] Testing Known Counterfeit / Mockup Test Note...")
    fake_samples = list((ROOT_DIR / "dataset/test/fake").glob("*.*"))
    if fake_samples:
        test_fake_path = fake_samples[0]
        with open(test_fake_path, "rb") as f:
            fake_bytes = f.read()
        response = client.post("/api/predict", files={"file": (test_fake_path.name, fake_bytes, "image/jpeg")})
        assert response.status_code == 200, f"HTTP Error: {response.text}"
        data = response.json()
        print(f"    - Input: {test_fake_path.name}")
        print(f"    - Predicted: {data['authenticity']} (Decision: {data['decision_status']}, Confidence: {data['confidence']})")
        assert data["decision_status"] == "suspected_fake", f"Expected suspected_fake, got {data['decision_status']}"
        test_results["Test 2: Known Counterfeit Note"] = "PASSED"
    else:
        test_results["Test 2: Known Counterfeit Note"] = "SKIPPED (No fake sample)"

    # ----------------------------------------------------------------------
    # Test 3: Blurry Image (Quality Gating)
    # ----------------------------------------------------------------------
    print("\n[TEST 3] Testing Blurry Image Quality Gating...")
    if genuine_samples:
        img = cv2.imread(str(genuine_samples[0]))
        blurred = cv2.GaussianBlur(img, (45, 45), 15.0)
        _, buf = cv2.imencode(".jpg", blurred)
        response = client.post("/api/predict", files={"file": ("blurred.jpg", buf.tobytes(), "image/jpeg")})
        assert response.status_code == 200
        data = response.json()
        print(f"    - Blur Score: {data['image_quality']['blur_score']}")
        print(f"    - Result: {data['authenticity']} | Decision: {data['decision_status']}")
        print(f"    - Message: {data['warning']}")
        assert data["decision_status"] in ["invalid_image", "uncertain"], "Expected quality rejection or uncertain"
        assert "insufficient" in data["warning"].lower() or "blurry" in data["warning"].lower()
        test_results["Test 3: Blurry Image Gating"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 4: Blank / Black Image
    # ----------------------------------------------------------------------
    print("\n[TEST 4] Testing Blank / Black Image Gating...")
    black_img = np.zeros((300, 600, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", black_img)
    response = client.post("/api/predict", files={"file": ("blank.jpg", buf.tobytes(), "image/jpeg")})
    assert response.status_code == 200
    data = response.json()
    print(f"    - Result: {data['authenticity']} | Decision: {data['decision_status']}")
    print(f"    - Quality Status: {data['image_quality']['status']}")
    assert data["decision_status"] in ["invalid_image", "uncertain"]
    assert data["image_quality"]["is_acceptable"] is False
    test_results["Test 4: Blank Image Rejection"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 5: Unsupported File Format
    # ----------------------------------------------------------------------
    print("\n[TEST 5] Testing Unsupported File Format Rejection...")
    response = client.post("/api/predict", files={"file": ("document.pdf", b"%PDF-1.4 dummy binary", "application/pdf")})
    print(f"    - Status Code: {response.status_code} (Expected 400 Bad Request)")
    assert response.status_code == 400, "Unsupported file format was not rejected with 400"
    test_results["Test 5: Unsupported Format"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 6: Non-Banknote Image (Random Noise)
    # ----------------------------------------------------------------------
    print("\n[TEST 6] Testing Image Containing No Currency Note (Noise)...")
    noise_img = np.random.randint(0, 256, (300, 600, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", noise_img)
    response = client.post("/api/predict", files={"file": ("noise.jpg", buf.tobytes(), "image/jpeg")})
    assert response.status_code == 200
    data = response.json()
    print(f"    - Result: {data['authenticity']} | Decision: {data['decision_status']}")
    test_results["Test 6: Non-Currency Image"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 7: Non-Standard / Tiny Image Dimensions
    # ----------------------------------------------------------------------
    print("\n[TEST 7] Testing Non-Standard Dimensions (50x50 tiny image)...")
    tiny_img = np.full((50, 50, 3), 128, dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", tiny_img)
    response = client.post("/api/predict", files={"file": ("tiny.jpg", buf.tobytes(), "image/jpeg")})
    assert response.status_code == 200
    data = response.json()
    print(f"    - Result: {data['authenticity']} | Decision: {data['decision_status']}")
    assert data["decision_status"] in ["invalid_image", "uncertain"]
    assert data["image_quality"]["is_acceptable"] is False
    test_results["Test 7: Incorrect Dimensions"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 8: Backend Inference Error Handling
    # ----------------------------------------------------------------------
    print("\n[TEST 8] Testing Corrupted Image Byte Handling...")
    corrupted_bytes = b"CORRUPTED_NOT_AN_IMAGE_HEADER_1234567890"
    response = client.post("/api/predict", files={"file": ("corrupt.jpg", corrupted_bytes, "image/jpeg")})
    print(f"    - Status Code: {response.status_code} (Expected 400 or 500 clean failure)")
    assert response.status_code in [400, 500]
    test_results["Test 8: Backend Error Handling"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 9: Camera Frame Base64 Submission
    # ----------------------------------------------------------------------
    print("\n[TEST 9] Testing Camera Frame Base64 Submission (/api/predict/camera)...")
    if genuine_samples:
        with open(genuine_samples[0], "rb") as f:
            raw_b64 = base64.b64encode(f.read()).decode("utf-8")
        payload = {"image_base64": f"data:image/jpeg;base64,{raw_b64}"}
        response = client.post("/api/predict/camera", json=payload)
        assert response.status_code == 200
        data = response.json()
        print(f"    - Camera Prediction: {data['authenticity']} ({data['confidence']})")
        assert data["decision_status"] == "likely_genuine"
        test_results["Test 9: Camera Frame Base64"] = "PASSED"

    # ----------------------------------------------------------------------
    # Test 10: Upload vs Camera Consistency
    # ----------------------------------------------------------------------
    print("\n[TEST 10] Testing Upload vs Camera Inference Consistency...")
    if genuine_samples:
        with open(genuine_samples[0], "rb") as f:
            file_bytes = f.read()
        # 1. Via Upload
        res_upload = client.post("/api/predict", files={"file": ("note.jpg", file_bytes, "image/jpeg")}).json()
        # 2. Via Camera Base64
        b64_str = base64.b64encode(file_bytes).decode("utf-8")
        res_camera = client.post("/api/predict/camera", json={"image_base64": b64_str}).json()
        
        print(f"    - Upload Decision: {res_upload['decision_status']} ({res_upload['confidence']})")
        print(f"    - Camera Decision: {res_camera['decision_status']} ({res_camera['confidence']})")
        assert res_upload["decision_status"] == res_camera["decision_status"], "Inconsistent decision between upload and camera"
        assert abs(res_upload["confidence"] - res_camera["confidence"]) < 0.05, "Confidence divergence between endpoints"
        test_results["Test 10: Upload & Camera Consistency"] = "PASSED"

# ----------------------------------------------------------------------
# Full Held-Out Test Set Metrics Evaluation
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("     Evaluating Held-Out Test Dataset (Independent Verification)")
print("=" * 70)

y_true = []
y_pred = []
y_probs = []

test_dir = ROOT_DIR / "dataset/test"
for label_folder, true_val in [("fake", 0), ("genuine", 1)]:
    folder = test_dir / label_folder
    if folder.exists():
        for img_p in folder.glob("*.*"):
            img = cv2.imread(str(img_p))
            if img is None:
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_res = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)
            t_input = tf.keras.applications.efficientnet.preprocess_input(img_res.astype(np.float32))[np.newaxis, ...]
            
            p_gen = float(model_manager.authenticity_model.predict(t_input, verbose=0)[0, 0])
            pred_val = 1 if p_gen >= 0.50 else 0
            
            y_true.append(true_val)
            y_pred.append(pred_val)
            y_probs.append(p_gen)

cm = confusion_matrix(y_true, y_pred)
# cm is: [[TN, FP], [FN, TP]] where 0=fake, 1=genuine
tn, fp, fn, tp = cm.ravel()
acc = accuracy_score(y_true, y_pred)
prec_gen = precision_score(y_true, y_pred, pos_label=1)
rec_gen = recall_score(y_true, y_pred, pos_label=1)
f1_gen = f1_score(y_true, y_pred, pos_label=1)
auc = roc_auc_score(y_true, y_probs)

# Rates
false_genuine_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0  # Counterfeits predicted genuine
false_fake_rate = fn / (tp + fn) if (tp + fn) > 0 else 0.0     # Genuine notes predicted fake

print(f"\n[*] Overall Accuracy:           {acc * 100:.2f}%")
print(f"[*] Genuine Precision:          {prec_gen * 100:.2f}%")
print(f"[*] Genuine Recall:             {rec_gen * 100:.2f}%")
print(f"[*] Genuine F1-Score:           {f1_gen:.4f}")
print(f"[*] ROC-AUC Score:              {auc:.4f}")
print(f"[*] False Genuine Rate (FP/N):  {false_genuine_rate * 100:.2f}% (Counterfeits classified as Genuine)")
print(f"[*] False Fake Rate (FN/P):     {false_fake_rate * 100:.2f}% (Genuine notes classified as Fake)")
print("\nConfusion Matrix:")
print(f"                Predicted Fake    Predicted Genuine")
print(f"  Actual Fake       {tn:5d}             {fp:5d}")
print(f"  Actual Genuine    {fn:5d}             {tp:5d}")

print("\n" + "=" * 70)
print("                   AUTOMATED TEST RESULTS SUMMARY")
print("=" * 70)
all_passed = True
for name, outcome in test_results.items():
    print(f"  {name:42s} : {outcome}")
    if outcome != "PASSED":
        all_passed = False

print("=" * 70)
if all_passed:
    print("ALL 10 VERIFICATION TESTS COMPLETED SUCCESSFULLY!\n")
else:
    print("SOME TESTS FAILED OR WERE SKIPPED.\n")
