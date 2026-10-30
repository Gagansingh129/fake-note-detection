import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

test_files = [
    ("Dummy/Churan Note", "dataset/raw/fake/dummy_churan_aug_0.jpg", "Suspected Fake"),
    ("Rs_10 Note", "dataset/test/genuine/note_denom_Rs_10_Rs_10_0138.jpg", "₹10"),
    ("Rs_20 Note", "dataset/test/genuine/note_denom_Rs_20_Rs_20_0171.jpg", "₹20"),
    ("Rs_50 Note", "dataset/test/genuine/note_denom_Rs_50_Rs_50_0200.jpg", "₹50"),
    ("Rs_100 Note", "dataset/test/genuine/note_denom_Rs_100_Rs_100_0224.jpg", "₹100"),
    ("Rs_200 Note", "dataset/test/genuine/note_denom_Rs_200_Rs_200_0249.jpg", "₹200"),
    ("Rs_500 Note", "dataset/raw/genuine/note_500_Rs_500_0120.jpg", "₹500"),
    ("Rs_2000 Note", "dataset/raw/genuine/note_2000_Rs_2000_0129.jpg", "₹2000"),
]

print("=" * 80)
print(f"{'Test Target':20} | {'Expected Denom/Auth':20} | {'Detected':10} | {'Authenticity (Conf)':25}")
print("=" * 80)

for label, filepath, expected in test_files:
    p = Path(filepath)
    if not p.exists():
        print(f"File not found: {filepath}")
        continue
    with open(p, "rb") as f:
        resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/jpeg")})
    res = resp.json()
    auth = res.get("authenticity")
    conf = res.get("confidence", 0) * 100
    denom = res.get("denomination")
    auth_str = f"{auth} ({conf:.1f}%)"
    print(f"{label:20} | {expected:20} | {denom:10} | {auth_str:25}")

print("=" * 80)
