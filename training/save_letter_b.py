import cv2
import numpy as np

img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
h, w = img.shape[:2]
y0, y1 = int(h * 0.62), int(h * 0.80)
x0, x1 = int(w * 0.19), int(w * 0.42)
serial_roi = img[y0:y1, x0:x1]

cv2.imwrite("backend/uploads/serial_roi_full.png", serial_roi)
cv2.imwrite("backend/uploads/letter_b_cropped.png", serial_roi[:, 65:115])
print("Saved letter_b_cropped.png")
