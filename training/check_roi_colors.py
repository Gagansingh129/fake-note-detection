import cv2
import numpy as np

roi = cv2.imread("backend/uploads/serial_roi.png")
print("ROI shape:", roi.shape)

# Let's check min and max BGR values
print("Min BGR:", np.min(roi, axis=(0,1)))
print("Mean BGR:", np.mean(roi, axis=(0,1)))
print("Max BGR:", np.max(roi, axis=(0,1)))

# Let's save color thresholded images to see how the text is rendered
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imwrite("backend/uploads/serial_thresh.png", thresh)

# Also let's inspect HSV of the digits
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# Find the characters by looking at the dark or colored pixels
print("Gray range:", np.min(gray), np.max(gray))
