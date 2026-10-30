import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict

# Test color characteristics of each denomination
denom_samples = defaultdict(list)
for p in Path('dataset/raw').glob('**/*.jpg'):
    for d in ["10", "20", "50", "100", "200", "500", "2000"]:
        if f"Rs_{d}" in p.name or f"_{d}_" in p.name:
            if len(denom_samples[d]) < 10:
                denom_samples[d].append(p)
            break

print("Testing color signatures for denominations:")
for denom, plist in sorted(denom_samples.items(), key=lambda x: int(x[0])):
    hues, sats, vals = [], [], []
    for p in plist:
        im = cv2.imread(str(p))
        if im is None:
            continue
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        h, s, v = np.mean(hsv[:, :, 0]), np.mean(hsv[:, :, 1]), np.mean(hsv[:, :, 2])
        hues.append(h)
        sats.append(s)
        vals.append(v)
    print(f"Rs_{denom:4s} ({len(plist)} samples) -> Mean Hue: {np.mean(hues):.1f}, Sat: {np.mean(sats):.1f}, Val: {np.mean(vals):.1f}")
