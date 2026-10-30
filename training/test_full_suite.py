import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

# Target real notes for each denomination
all_targets = ["Rs_10", "Rs_20", "Rs_50", "Rs_100", "Rs_200", "Rs_500", "Rs_2000"]
matched_files = {}

for p in Path("dataset").glob("**/*.jpg"):
    # exact denomination regex match
    m = re.search(r'(?:^|[_\/\\])(Rs_2000|Rs_500|Rs_200|Rs_100|Rs_50|Rs_20|Rs_10)(?:[_\/\.\\]|$)', str(p))
    if m:
        denom = m.group(1)
        if denom not in matched_files:
            matched_files[denom] = p

print("=" * 80)
print(f"{'Target Denom':14} | {'Test Image File':36} | {'Detected':8} | {'Authenticity'}")
print("=" * 80)

for d in all_targets:
    if d in matched_files:
        p = matched_files[d]
        with open(p, "rb") as f:
            resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/jpeg")})
        res = resp.json()
        det = res.get("denomination")
        auth = res.get("authenticity")
        conf = res.get("confidence", 0) * 100
        print(f"{d:14} | {p.name[:36]:36} | {det:8} | {auth} ({conf:.1f}%)")

# Test Dummy / Churan note
dummy_p = Path("dataset/raw/fake/note_dummy_fulloffun_camera_1_aug_001.jpg")
if dummy_p.exists():
    with open(dummy_p, "rb") as f:
        resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (dummy_p.name, f, "image/jpeg")})
    res = resp.json()
    det = res.get("denomination")
    auth = res.get("authenticity")
    conf = res.get("confidence", 0) * 100
    print(f"{'Dummy/Churan':14} | {dummy_p.name[:36]:36} | {det:8} | {auth} ({conf:.1f}%)")

print("=" * 80)
