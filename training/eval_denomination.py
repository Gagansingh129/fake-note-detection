import json
import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path

with open('backend/models/class_names.json', 'r') as f:
    class_names = json.load(f)

denom_classes = class_names['denomination']
print('Classes in registry:', denom_classes)

model = tf.keras.models.load_model('backend/models/denomination_model.keras')

denoms_desc = ['Rs_2000', 'Rs_500', 'Rs_200', 'Rs_100', 'Rs_50', 'Rs_20', 'Rs_10']

chosen = {d: [] for d in denoms_desc}
for p in Path('dataset').glob('**/*.jpg'):
    for d in denoms_desc:
        if d in p.name or f"/{d.replace('Rs_','')}/" in str(p).replace('\\','/'):
            if len(chosen[d]) < 2:
                chosen[d].append(p)
            break

print("\n--- Model Predictions on Test Samples for All 7 Denominations ---")
total_correct = 0
total_tested = 0
for expected, paths in chosen.items():
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = cv2.resize(rgb, (224, 224))
        t_in = tf.keras.applications.efficientnet.preprocess_input(res.astype(np.float32))[np.newaxis, ...]
        preds = model.predict(t_in, verbose=0)[0]
        best_idx = int(np.argmax(preds))
        pred_class = denom_classes[best_idx]
        conf = float(preds[best_idx])
        is_match = (expected == pred_class)
        if is_match:
            total_correct += 1
        total_tested += 1
        print(f"File: {p.name[:32]:32} | Expected: {expected:7} | Predicted: {pred_class:7} ({conf*100:5.1f}%) | {'MATCH' if is_match else 'DIFF'}")

print(f"\nOverall Denomination Accuracy on Sample Evaluation: {total_correct}/{total_tested} ({total_correct/total_tested*100:.1f}%)")
