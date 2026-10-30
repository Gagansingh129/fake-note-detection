import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

# 1. Test User's Note with Alphabet in Serial
p = Path("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
with open(p, "rb") as f:
    resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/png")})

res = resp.json()
print("=" * 70)
print("TEST ON USER NOTE (NOTE WITH ALPHABET IN SERIAL NUMBER):")
print(f"  Decision Status:     {res.get('decision_status')}")
print(f"  Authenticity Label:  {res.get('authenticity')}")
print(f"  Overall Confidence:  {res.get('confidence',0)*100:.1f}%")
print(f"  Fake Score:          {res.get('fake_score',0)*100:.1f}%")
print(f"  Genuine Score:       {res.get('genuine_score',0)*100:.1f}%")
print(f"  Detected Denom:      {res.get('denomination')}")
print("=" * 70)

# 2. Test Real Banknotes to ensure they still pass as Likely Genuine
test_samples = [
    ("Real 50 Note", "dataset/test/genuine/note_denom_Rs_50_Rs_50_0200.jpg"),
    ("Real 100 Note", "dataset/test/genuine/note_denom_Rs_100_Rs_100_0224.jpg"),
    ("Real 500 Note", "dataset/raw/genuine/note_500_Rs_500_0120.jpg"),
    ("Dummy / Churan Note", "C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1792659135668_082e1f3d.png")
]

print("\nCORROBORATION SUITE:")
for label, path in test_samples:
    tp = Path(path)
    if tp.exists():
        with open(tp, "rb") as f:
            r = requests.post(f"{BASE_URL}/api/predict", files={"file": (tp.name, f, "image/jpeg")}).json()
        print(f"  {label:20} -> {r.get('denomination'):6} | {r.get('authenticity'):15} (Fake: {r.get('fake_score',0)*100:5.1f}%, Gen: {r.get('genuine_score',0)*100:5.1f}%)")
print("=" * 70)
