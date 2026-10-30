import cv2
import numpy as np

img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
h, w = img.shape[:2]

# Serial number on bottom-left:
# x: ~18% to 45%, y: ~65% to ~85%
x0, x1 = int(w * 0.18), int(w * 0.44)
y0, y1 = int(h * 0.62), int(h * 0.82)
roi = img[y0:y1, x0:x1]
cv2.imwrite("backend/uploads/serial_roi.png", roi)

# Let's inspect the red digits in the serial number:
# Red color in BGR: high R, low B and G
b, g, r = cv2.split(roi)
red_mask = (r.astype(np.int32) - np.maximum(b, g).astype(np.int32) > 30) & (r > 80)
cv2.imwrite("backend/uploads/serial_red_mask.png", (red_mask * 255).astype(np.uint8))

print("Red mask pixel count:", np.sum(red_mask))
print("ROI shape:", roi.shape)

# Let's see what is between 2MA and 384765 in the red mask / image:
# 2MA is on the left, 384765 is on the right.
# Between them is a character 'B'!
