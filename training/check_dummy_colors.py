import cv2
import numpy as np

img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1792659135668_082e1f3d.png")
h, w = img.shape[:2]
cx0, cx1 = int(w * 0.20), int(w * 0.80)
cy0, cy1 = int(h * 0.20), int(h * 0.80)
roi = img[cy0:cy1, cx0:cx1]
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
h_chan, s_chan = hsv[:, :, 0], hsv[:, :, 1]
total_px = max(1, roi.shape[0] * roi.shape[1])

cyan_pct = float(np.sum((h_chan >= 85) & (h_chan <= 118) & (s_chan >= 40))) / total_px
orange_pct = float(np.sum((h_chan >= 12) & (h_chan <= 30) & (s_chan >= 70))) / total_px
print(f"Dummy note: cyan_pct = {cyan_pct:.4f}, orange_pct = {orange_pct:.4f}")
