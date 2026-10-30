import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path
import json

with open('backend/models/class_names.json', 'r') as f:
    class_names = json.load(f)

denom_classes = class_names['denomination']
print('Denomination classes:', denom_classes)

model = tf.keras.models.load_model('backend/models/denomination_model.keras')

# Test on test samples
test_dir = Path('dataset/test')
for p in list(test_dir.glob('**/*.jpg'))[:15]:
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
    print(f'{p.name} -> Pred: {pred_class} ({conf*100:.1f}%)')
