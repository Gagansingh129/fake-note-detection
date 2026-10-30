import cv2
import numpy as np

img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
h, w = img.shape[:2]

x0, x1 = int(w * 0.65), int(w * 0.90)
y0, y1 = int(h * 0.50), int(h * 0.85)
roi = img[y0:y1, x0:x1]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
rh, rw = roi.shape[:2]

glyphs = []
for i in range(1, num_labels):
    x, y, cw, ch, area = stats[i]
    if rh * 0.25 <= ch <= rh * 0.80 and 0.15 <= cw / ch <= 1.2 and area > 100:
        glyphs.append((x, y, cw, ch, area))

glyphs.sort(key=lambda d: d[0])
print(f"Extracted {len(glyphs)} glyphs:")
for idx, d in enumerate(glyphs):
    print(f"  Glyph {idx}: x={d[0]}, y={d[1]}, w={d[2]}, h={d[3]}, aspect={d[2]/d[3]:.2f}, area={d[4]}")
