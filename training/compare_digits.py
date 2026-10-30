import cv2
import numpy as np

roi = cv2.imread("backend/uploads/crop_denom_1000.jpg")
digit_1 = roi[21:21+51, 53:53+20]
cv2.imwrite("backend/uploads/digit_1_extracted.png", digit_1)

# Now check real 2000 note from dataset
real_2000 = cv2.imread("dataset/raw/genuine/note_2000_Rs_2000_0129.jpg")
h, w = real_2000.shape[:2]
roi_2000 = real_2000[int(h*0.50):int(h*0.85), int(w*0.65):int(w*0.88)]
cv2.imwrite("backend/uploads/crop_denom_2000.jpg", roi_2000)

print("Saved digit_1_extracted.png and crop_denom_2000.jpg")
