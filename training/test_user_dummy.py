import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
p = Path("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1792659135668_082e1f3d.png")

with open(p, "rb") as f:
    resp = requests.post(f"{BASE_URL}/api/predict", files={"file": (p.name, f, "image/png")})

res = resp.json()
print("User Dummy Note Test:")
print("  Status:", res.get("decision_status"))
print("  Authenticity:", res.get("authenticity"))
print("  Confidence:", f"{res.get('confidence',0)*100:.1f}%")
print("  Fake Score:", f"{res.get('fake_score',0)*100:.1f}%")
print("  Denomination:", res.get("denomination"))
