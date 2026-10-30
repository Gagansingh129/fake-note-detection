import cv2
import numpy as np
import tensorflow as tf
import json

img = cv2.imread("backend/uploads/user_camera_note_100.jpg")
h, w = img.shape[:2]

# 1. Denomination model prediction
model = tf.keras.models.load_model("backend/models/denomination_model.keras")
with open("backend/models/class_names.json", "r") as f:
    class_names = json.load(f)["denomination"]

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
resized = cv2.resize(rgb, (224, 224))
tensor_in = tf.keras.applications.efficientnet.preprocess_input(resized.astype(np.float32))[np.newaxis, ...]
preds = model.predict(tensor_in, verbose=0)[0]

print("Denomination model predictions:")
for name, p in zip(class_names, preds):
    print(f"  {name:8}: {p*100:5.2f}%")

# 2. Check color features in corroborate_denomination
cx0, cx1 = int(w * 0.20), int(w * 0.80)
cy0, cy1 = int(h * 0.20), int(h * 0.80)
roi = img[cy0:cy1, cx0:cx1]
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
h_chan, s_chan = hsv[:, :, 0], hsv[:, :, 1]
total_px = max(1, roi.shape[0] * roi.shape[1])

mean_sat = float(np.mean(s_chan))
cyan_pct = float(np.sum((h_chan >= 85) & (h_chan <= 118) & (s_chan >= 40))) / total_px
magenta_pct = float(np.sum((h_chan >= 145) & (h_chan <= 175) & (s_chan >= 40))) / total_px
orange_pct = float(np.sum((h_chan >= 12) & (h_chan <= 30) & (s_chan >= 70))) / total_px
lavender_pct = float(np.sum((h_chan >= 120) & (h_chan <= 145) & (s_chan >= 35))) / total_px

print(f"\nColor metrics:")
print(f"  mean_sat:     {mean_sat:.2f}")
print(f"  cyan_pct:     {cyan_pct*100:.2f}%")
print(f"  magenta_pct:  {magenta_pct*100:.2f}%")
print(f"  orange_pct:   {orange_pct*100:.2f}%")
print(f"  lavender_pct: {lavender_pct*100:.2f}%")
