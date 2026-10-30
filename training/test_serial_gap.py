import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
h, w = img.shape[:2]

# Let's crop the bottom left serial region:
x0, x1 = int(w * 0.18), int(w * 0.44)
y0, y1 = int(h * 0.62), int(h * 0.82)
serial_roi = img[y0:y1, x0:x1]

# In authentic notes, the gap between prefix (e.g. 2MA) and 6-digit number (384765) is either clean space or uniform background.
# In this fake note, right between the prefix and the number (around 35%-50% of the ROI width), there is an alphabet letter 'B'!
# Let's inspect the vertical projection / gradients in this middle column:
roi_w = serial_roi.shape[1]
mid_x0 = int(roi_w * 0.28)
mid_x1 = int(roi_w * 0.50)
mid_roi = serial_roi[:, mid_x0:mid_x1]

cv2.imwrite("backend/uploads/mid_letter_b.png", mid_roi)
print("Mid ROI shape:", mid_roi.shape)

# Let's inspect edges and intensity variance in this middle zone
gray_mid = cv2.cvtColor(mid_roi, cv2.COLOR_BGR2GRAY)
sobel_mid = cv2.Sobel(gray_mid, cv2.CV_64F, 1, 1, ksize=3)
gradient_energy = np.mean(np.abs(sobel_mid))
print("Gradient energy in serial gap:", gradient_energy)
