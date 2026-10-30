from pathlib import Path
from collections import Counter
import re

for partition in ['dataset/train', 'dataset/raw']:
    found = Counter()
    for p in Path(partition).glob('**/*.jpg'):
        for d in ["2000", "500", "200", "100", "50", "20", "10"]:
            if f"Rs_{d}" in p.name or f"_{d}_" in p.name or f"note_{d}_" in p.name:
                found[d] += 1
                break
    print(partition, dict(found))
