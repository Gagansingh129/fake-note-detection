import cv2
import numpy as np

img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
h, w = img.shape[:2]

# Bottom left serial region for Mahatma Gandhi series:
# y: 62% to 80%, x: 19% to 42%
y0, y1 = int(h * 0.62), int(h * 0.80)
x0, x1 = int(w * 0.19), int(w * 0.42)
serial_roi = img[y0:y1, x0:x1]

# In this serial_roi:
# Text: 2MA   B   384765
# Let's inspect the text components
gray = cv2.cvtColor(serial_roi, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)

# The red serial digits have a distinct chromatic signature:
b, g, r = cv2.split(serial_roi)
# Red ink has higher R than G and B
redness = r.astype(np.float32) - (g.astype(np.float32) + b.astype(np.float32)) / 2.0
red_mask = (redness > 15) & (r > 60)

# But notice the 'B' letter in the background:
# It is printed in grey/black outline or shaded letter!
# Let's see the B letter in gray/edges:
edges = cv2.Canny(gray, 40, 120)

# Look at the column-wise profile (vertical projection) across the serial ROI
col_edges = np.sum(edges, axis=0)
col_red = np.sum(red_mask, axis=0)

print("ROI width:", serial_roi.shape[1], "ROI height:", serial_roi.shape[0])

# In this note, between the prefix '2MA' (cols 0-70) and '384765' (cols 110-230):
# cols 70 to 110 contain the letter 'B'!
gap_edges = edges[:, 70:110]
print("Edge count in letter 'B' gap (70:110):", np.sum(gap_edges > 0))

# Contrast this with a genuine note where the gap between prefix and digits has no letter:
# Let's test on several notes
