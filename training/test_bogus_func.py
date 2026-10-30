import cv2
import numpy as np
import sys, os
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.security_features import check_for_bogus_1000_numeral

img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
flag, score = check_for_bogus_1000_numeral(img)
print("Result on user_camera_bogus_note.jpg:", flag, score)
