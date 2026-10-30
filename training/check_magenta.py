import cv2
import numpy as np

img = cv2.imread("dataset/raw/genuine/note_denom_Rs_100_Rs_100_0224.jpg")
h, w = img.shape[:2]
cx0, cx1 = int(w * 0.20), int(w * 0.80)
cy0, cy1 = int(h * 0.20), int(h * 0.80)
roi = img[cy0:cy1, cx0:cx1]
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
h_chan, s_chan = hsv[:, :, 0], hsv[:, :, 1]
total_px = max(1, roi.shape[0] * roi.shape[1])

magenta_pct = float(np.sum((h_chan >= 145) & (h_chan <= 175) & (s_chan >= 40))) / total_px
lavender_pct = float(np.sum((h_chan >= 120) & (h_chan <= 145) & (s_chan >= 35))) / total_px
print(f"note_denom_Rs_100: magenta_pct = {magenta_pct:.4f}, lavender_pct = {lavender_pct:.4f}")

# Check real 2000 note
r2000 = cv2.imread("dataset/raw/genuine/note_2000_Rs_2000_0129.jpg")
h2, w2 = r2000.shape[:2]
roi2 = r2000[int(h2*0.2):int(h2*0.8), int(w2*0.2):int(w2*0.8)]
hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
h2_chan, s2_chan = hsv2[:, :, 0], hsv2[:, :, 1]
tot2 = max(1, roi2.shape[0] * roi2.shape[1])
mag2 = float(np.sum((h2_chan >= 145) & (h2_chan <= 175) & (s2_chan >= 40))) / tot2
print(f"note_2000: magenta_pct = {mag2:.4f}")
