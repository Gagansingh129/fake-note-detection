import cv2
import numpy as np

tpl = cv2.imread("backend/models/template_100.png")
gray_tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

for p in [
    "dataset/test/genuine/note_denom_Rs_50_Rs_50_0200.jpg",
    "dataset/raw/genuine/note_500_Rs_500_0120.jpg",
    "dataset/raw/genuine/note_2000_Rs_2000_0129.jpg",
    "dataset/raw/genuine/note_denom_Rs_100_Rs_100_0224.jpg"
]:
    img = cv2.imread(p)
    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_img, gray_tpl, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, _ = cv2.minMaxLoc(res)
        print(f"{p[:35]:35}: max correlation = {max_v:.4f}")
