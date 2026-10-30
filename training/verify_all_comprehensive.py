import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

test_cases = [
    ("User Bogus ₹1000 Note", "backend/uploads/user_camera_bogus_note.jpg", "₹1000", "Suspected Fake"),
    ("Fake Note Alphabet in Serial", "C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png", "₹100", "Suspected Fake"),
    ("Dummy / Churan Note", "C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1792659135668_082e1f3d.png", "₹200", "Suspected Fake"),
    ("Real ₹50 Note", "dataset/test/genuine/note_denom_Rs_50_Rs_50_0200.jpg", "₹50", "Likely Genuine"),
    ("Real ₹100 Note", "dataset/test/genuine/note_denom_Rs_100_Rs_100_0224.jpg", "₹100", "Likely Genuine"),
    ("Real ₹500 Note", "dataset/raw/genuine/note_500_Rs_500_0120.jpg", "₹500", "Likely Genuine"),
    ("Real ₹2000 Note", "dataset/raw/genuine/note_2000_Rs_2000_0129.jpg", "₹2000", "Likely Genuine"),
]

print("=" * 86)
print(f"{'Target Test Case':30} | {'Expected Denom':14} | {'Detected':10} | {'Authenticity (Score)'}")
print("=" * 86)

for label, filepath, exp_denom, exp_auth in test_cases:
    p = Path(filepath)
    if not p.exists():
        print(f"File not found: {filepath}")
        continue
    with open(p, "rb") as f:
        resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/jpeg" if p.suffix.lower() == ".jpg" else "image/png")})
    res = resp.json()
    det_denom = res.get("denomination")
    auth = res.get("authenticity")
    conf = res.get("confidence", 0) * 100
    fake_s = res.get("fake_score", 0) * 100
    gen_s = res.get("genuine_score", 0) * 100
    status = "MATCH" if (det_denom == exp_denom and auth == exp_auth) else "DIFF"
    print(f"{label:30} | {exp_denom:14} | {det_denom:10} | {auth} (Fake: {fake_s:.1f}%, Gen: {gen_s:.1f}%) [{status}]")

print("=" * 86)
