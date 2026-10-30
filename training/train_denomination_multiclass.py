"""
NoteGuard AI - 9-Class Denomination Classifier Training Pipeline
================================================================
Trains a dedicated multi-class Transfer Learning classifier to recognize
all 9 Indian Currency denominations:
    ₹5, ₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹1000, ₹2000

Includes:
- Training on both Obverse (Front) and Reverse (Back) designs.
- Two-phase training: Head training + Fine-tuning.
- Test partition evaluation with full Confusion Matrix, Precision, Recall, and F1 metrics.
- Export to backend/models/denomination_model.keras and backend/models/class_names.json.
"""

import os
import sys

# Ensure UTF-8 output and clean environment
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
os.environ.pop("HOME", None)
os.environ["USERPROFILE"] = "C:\\Users\\LOQ"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import json
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

mpl_dir = os.path.join(tempfile.gettempdir(), "matplotlib_noteguard")
os.makedirs(mpl_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_dir

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import cv2

DENOM_CLASSES = ["5", "10", "20", "50", "100", "200", "500", "1000", "2000"]

def load_split(split_dir: Path, target_size=(224, 224)) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Loads all images and integer class labels from directory."""
    images = []
    labels = []
    for idx, d in enumerate(DENOM_CLASSES):
        fldr = split_dir / d
        if not fldr.exists():
            continue
        for p in fldr.glob("*.jpg"):
            img = cv2.imread(str(p))
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if img_rgb.shape[:2] != target_size:
                    img_rgb = cv2.resize(img_rgb, target_size)
                images.append(img_rgb)
                labels.append(idx)
    return np.array(images, dtype=np.float32), np.array(labels, dtype=np.int32), DENOM_CLASSES

def plot_confusion_matrix(cm: np.ndarray, classes: List[str], output_path: Path):
    """Plots and saves the multiclass confusion matrix."""
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    tick_marks = np.arange(len(classes))
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.set_xticklabels([f"₹{c}" for c in classes], rotation=45, ha="right", fontsize=9, fontweight="bold")
    ax.set_yticklabels([f"₹{c}" for c in classes], fontsize=9, fontweight="bold")
    ax.set_ylabel("True Denomination", fontsize=11, fontweight="bold")
    ax.set_xlabel("Predicted Denomination", fontsize=11, fontweight="bold")
    ax.set_title("Indian Currency Denomination Confusion Matrix", fontsize=12, fontweight="bold")

    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontweight="bold")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(str(output_path), dpi=200)
    plt.close()
    print(f"[*] Confusion matrix saved to: {output_path}")

def train_multiclass_model(
    dataset_base: Path = Path("dataset/denomination"),
    output_model_path: Path = Path("backend/models/denomination_model.keras"),
    classes_json_path: Path = Path("backend/models/class_names.json"),
    epochs_head: int = 6,
    epochs_fine: int = 4,
    batch_size: int = 16
):
    print("=" * 65)
    print("  NoteGuard AI: Training Dedicated Denomination Classifier  ")
    print("=" * 65)

    # 1. Load Data
    X_train, y_train, classes = load_split(dataset_base / "train")
    X_val, y_val, _ = load_split(dataset_base / "validation")
    X_test, y_test, _ = load_split(dataset_base / "test")

    print(f"[*] Training samples   : {len(X_train)}")
    print(f"[*] Validation samples : {len(X_val)}")
    print(f"[*] Test samples       : {len(X_test)}")
    print(f"[*] Denomination classes ({len(classes)}): {classes}")

    # Normalization using EfficientNet preprocess_input
    X_train_norm = tf.keras.applications.efficientnet.preprocess_input(X_train)
    X_val_norm = tf.keras.applications.efficientnet.preprocess_input(X_val)
    X_test_norm = tf.keras.applications.efficientnet.preprocess_input(X_test)

    # Compute class weights to handle slight variations
    from sklearn.utils.class_weight import compute_class_weight
    class_weights_arr = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
    class_weights = {i: float(w) for i, w in zip(np.unique(y_train), class_weights_arr)}

    # 2. Build Model
    base_model = tf.keras.applications.EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False

    inputs = tf.keras.layers.Input(shape=(224, 224, 3), name="input_banknote")
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="gap")(x)
    x = tf.keras.layers.BatchNormalization(name="head_bn")(x)
    x = tf.keras.layers.Dropout(0.35, name="head_dropout")(x)
    x = tf.keras.layers.Dense(128, activation="relu", name="head_dense")(x)
    x = tf.keras.layers.Dropout(0.25, name="head_dropout2")(x)
    outputs = tf.keras.layers.Dense(len(classes), activation="softmax", name="denomination_probabilities")(x)

    model = tf.keras.models.Model(inputs=inputs, outputs=outputs, name="noteguard_denomination_net")

    # Phase 1: Train Head
    print("\n--- Phase 1: Training Classification Head ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    history1 = model.fit(
        X_train_norm, y_train,
        validation_data=(X_val_norm, y_val),
        epochs=epochs_head,
        batch_size=batch_size,
        class_weight=class_weights,
        verbose=1
    )

    # Phase 2: Fine-Tuning top layers of EfficientNetB0
    print("\n--- Phase 2: Fine-Tuning Upper Convolutional Layers ---")
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    for layer in base_model.layers:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    history2 = model.fit(
        X_train_norm, y_train,
        validation_data=(X_val_norm, y_val),
        epochs=epochs_fine,
        batch_size=batch_size,
        class_weight=class_weights,
        verbose=1
    )

    # 3. Evaluate on Independent Test Set
    print("\n" + "=" * 65)
    print("  Test Partition Evaluation (Independent Unseen Banknotes)  ")
    print("=" * 65)
    preds = model.predict(X_test_norm, verbose=0)
    pred_labels = np.argmax(preds, axis=1)

    test_acc = np.mean(pred_labels == y_test)
    print(f"\n[*] Overall Test Accuracy: {test_acc * 100:.2f}%\n")

    target_names = [f"₹{c}" for c in classes]
    report = classification_report(y_test, pred_labels, target_names=target_names, digits=4)
    print("Classification Report:")
    print(report)

    # Save classification report as text
    report_path = Path("results/denomination_classification_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("NoteGuard AI - 9-Class Denomination Classifier Test Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Test Accuracy: {test_acc * 100:.2f}%\n\n")
        f.write(report)
    print(f"[*] Report saved to: {report_path}")

    # Plot Confusion Matrix
    cm = confusion_matrix(y_test, pred_labels)
    cm_path = Path("results/graphs/denomination_multiclass_confusion_matrix.png")
    plot_confusion_matrix(cm, classes, cm_path)

    # 4. Save Model & Registry
    output_model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(output_model_path))
    print(f"[*] Denomination model saved to: {output_model_path}")

    # Update class_names.json registry
    registry = {}
    if classes_json_path.exists():
        try:
            with open(classes_json_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception:
            registry = {}
    registry["denomination"] = [f"Rs_{c}" for c in classes]
    with open(classes_json_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
    print(f"[*] Updated denomination classes in registry: {registry['denomination']}")

    print("=" * 65)
    print("  Denomination Model Training Completed Successfully!  ")
    print("=" * 65)

if __name__ == "__main__":
    train_multiclass_model()

