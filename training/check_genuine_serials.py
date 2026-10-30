import cv2
import numpy as np
from pathlib import Path

# Check genuine notes of Mahatma Gandhi series (where serial is on bottom-left)
# or new series
for p in list(Path("dataset").glob("**/*100*.jpg"))[:5]:
    img = cv2.imread(str(p))
    if img is None:
        continue
    h, w = img.shape[:2]
    # bottom left
    y0, y1 = int(h * 0.62), int(h * 0.80)
    x0, x1 = int(w * 0.19), int(w * 0.42)
    roi = img[y0:y1, x0:x1]
    if roi.size == 0:
        continue
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    # Check middle third of ROI
    rw = roi.shape[1]
    mid = edges[:, int(rw*0.30):int(rw*0.50)]
    print(f"{p.name[:30]:30} | shape: {roi.shape} | mid edge count: {np.sum(mid > 0)}")
