import re
from pathlib import Path

def get_true_denomination(path: Path):
    parts = [p.lower() for p in path.parts]
    # Check if inside denomination-specific folder
    for p in parts:
        clean = p.replace("rs_", "")
        if clean in ["10", "20", "50", "100", "200", "500", "2000"]:
            return f"Rs_{clean}"
    
    # Check if explicit denomination token in filename:
    # Must be 'Rs_X' or 'note_X_' where X is the denomination, NOT a trailing index!
    m = re.search(r'(?:^|[_\/\\])Rs_(2000|1000|500|200|100|50|20|10)(?:[_\/\.\\]|$)', path.name, re.IGNORECASE)
    if m:
        return f"Rs_{m.group(1)}"
        
    m2 = re.search(r'^note_(2000|1000|500|200|100|50|20|10)_', path.name, re.IGNORECASE)
    if m2:
        return f"Rs_{m2.group(1)}"
        
    # Check for fake note with alphabet in serial: that note is Rs_100!
    if "fake_alphabet_in_serial" in path.name:
        return "Rs_100"

    # Check for fake bogus 1000: that note is Rs_1000!
    if "bogus_1000" in path.name:
        return "Rs_1000"

    return None

from collections import Counter
for folder in ["dataset/train", "dataset/validation", "dataset/raw"]:
    c = Counter()
    for p in Path(folder).glob("**/*.*"):
        if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            d = get_true_denomination(p)
            if d:
                c[d] += 1
            else:
                c["Unknown"] += 1
    print(folder, dict(c))
