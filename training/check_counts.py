from pathlib import Path
import re
from collections import Counter

for folder in ["dataset/raw/genuine", "dataset/raw/fake", "dataset/train", "dataset/validation", "dataset/test"]:
    p = Path(folder)
    c = Counter()
    for f in p.glob("**/*.*"):
        if f.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            denom = "Unknown"
            for part in f.parts:
                cp = part.replace("Rs_", "")
                if cp in ["10", "20", "50", "100", "200", "500", "2000"]:
                    denom = f"Rs_{cp}"
                    break
            if denom == "Unknown":
                m = re.search(r'(?:Rs_|_)?(2000|500|200|100|50|20|10)(?:_|\.|$)', f.name)
                if m:
                    denom = f"Rs_{m.group(1)}"
            c[denom] += 1
    print(folder, dict(c))
