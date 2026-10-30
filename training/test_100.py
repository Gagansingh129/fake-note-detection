import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

p = Path("dataset/raw/genuine/note_denom_Rs_100_Rs_100_0224.jpg")
with open(p, "rb") as f:
    resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/jpeg")})
res = resp.json()
print("Real ₹100 Note:", res.get("denomination"), res.get("authenticity"), f"Fake: {res.get('fake_score',0)*100:.1f}%, Gen: {res.get('genuine_score',0)*100:.1f}%")
