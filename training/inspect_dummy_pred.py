import sys
sys.stdout.reconfigure(encoding='utf-8')
import cv2
import requests
from pathlib import Path

dummy_p = Path("dataset/raw/fake/note_dummy_fulloffun_camera_1_aug_001.jpg")
resp = requests.post("http://127.0.0.1:8000/api/predict", files={"file": (dummy_p.name, open(dummy_p, "rb"), "image/jpeg")})
res = resp.json()
print("Keys:", list(res.keys()))
print("decision_status:", res.get("decision_status"))
print("authenticity:", res.get("authenticity"))
print("warning:", res.get("warning"))
print("image_quality:", res.get("image_quality"))
print("genuine_score:", res.get("genuine_score"))
print("fake_score:", res.get("fake_score"))
