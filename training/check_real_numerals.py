import sys, os
sys.path.append(os.getcwd())
import cv2
import numpy as np
from training.test_denom_extract import extract_denomination_numeral

real_2000 = cv2.imread("dataset/raw/genuine/note_2000_Rs_2000_0129.jpg")
res_2000 = extract_denomination_numeral(real_2000)
print("Real 2000 Note Numeral Zone:", res_2000)

real_500 = cv2.imread("dataset/raw/genuine/note_500_Rs_500_0120.jpg")
res_500 = extract_denomination_numeral(real_500)
print("Real 500 Note Numeral Zone:", res_500)
