import cv2
import numpy as np

img_path = "C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png"
img = cv2.imread(img_path)
h, w, _ = img.shape
print("Image size:", w, h)

# Crop the bottom left serial number area
crop = img[int(h*0.55):int(h*0.85), int(w*0.15):int(w*0.50)]
cv2.imwrite("backend/uploads/crop_serial.jpg", crop)
print("Cropped serial saved to backend/uploads/crop_serial.jpg")

# Also test model prediction on this uploaded image
import requests
resp = requests.post("http://127.0.0.1:8000/api/predict", files={"file": ("test_user_note.png", open(img_path, "rb"), "image/png")})
res = resp.json()
print("Prediction Result:")
print("  Authenticity:", res.get("authenticity"))
print("  Status:", res.get("decision_status"))
print("  Confidence:", f"{res.get('confidence',0)*100:.1f}%")
print("  Genuine Score:", f"{res.get('genuine_score',0)*100:.1f}%")
print("  Fake Score:", f"{res.get('fake_score',0)*100:.1f}%")
print("  Denomination:", res.get("denomination"))
print("  Security features:", res.get("security_features"))
