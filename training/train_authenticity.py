"""
NoteGuard AI - Stage 2: Authenticity Classifier Training (EfficientNetB0)
========================================================================
Implements Transfer Learning with EfficientNetB0 for screening whether an
Indian currency note appears Genuine or Counterfeit.

Training Procedure:
Phase 1: Feature Extraction (Pretrained ImageNet base frozen, train head)
Phase 2: Fine-Tuning (Unfreeze top 20 layers with fine-tune learning rate 1e-5)
"""

import os
import sys
import tempfile

os.environ.pop("HOME", None)
os.environ["USERPROFILE"] = "C:\\Users\\LOQ"
mpl_dir = os.path.join(tempfile.gettempdir(), "matplotlib_noteguard")
os.makedirs(mpl_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_dir
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from training.models import build_efficientnet_model
from training.dataset_loader import load_dataset_tf


def plot_combined_history(history1, history2, output_path: Path):
    """Combines Phase 1 and Phase 2 training curves into a continuous trajectory."""
    acc = history1.history.get("accuracy", [])
    val_acc = history1.history.get("val_accuracy", [])
    loss = history1.history.get("loss", [])
    val_loss = history1.history.get("val_loss", [])

    if history2:
        acc += history2.history.get("accuracy", [])
        val_acc += history2.history.get("val_accuracy", [])
        loss += history2.history.get("loss", [])
        val_loss += history2.history.get("val_loss", [])

    epochs = range(1, len(acc) + 1)
    split_epoch = len(history1.history.get("accuracy", []))

    plt.figure(figsize=(12, 5))

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, "b-o", label="Training Accuracy")
    plt.plot(epochs, val_acc, "g--s", label="Validation Accuracy")
    if history2 and len(history2.history.get("accuracy", [])) > 0:
        plt.axvline(x=split_epoch, color="red", linestyle=":", label="Fine-Tuning Start")
    plt.title("Authenticity (EfficientNetB0) - Accuracy", fontsize=11, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.ylim([0, 1.05])
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, "b-o", label="Training Loss")
    plt.plot(epochs, val_loss, "r--s", label="Validation Loss")
    if history2 and len(history2.history.get("loss", [])) > 0:
        plt.axvline(x=split_epoch, color="red", linestyle=":", label="Fine-Tuning Start")
    plt.title("Authenticity (EfficientNetB0) - Loss", fontsize=11, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"[*] Training graph saved to: {output_path}")


def train_authenticity(
    train_dir: str = "dataset/train",
    val_dir: str = "dataset/validation",
    epochs_head: int = 5,
    epochs_finetune: int = 3,
    batch_size: int = 16,
    initial_lr: float = 0.001,
    finetune_lr: float = 0.00001,
    output_model_path: str = "backend/models/authenticity_model.keras"
):
    print("=" * 65)
    print("    NoteGuard AI - Training Stage 2: Authenticity Classifier    ")
    print("=" * 65)

    # 1. Load Data
    train_ds, class_names, class_weights = load_dataset_tf(
        train_dir, task="authenticity", batch_size=batch_size, is_training=True, normalization="efficientnet"
    )
    val_ds, _, _ = load_dataset_tf(
        val_dir, task="authenticity", batch_size=batch_size, is_training=False, normalization="efficientnet"
    )

    num_classes = len(class_names)
    print(f"[*] Authenticity Classes: {class_names} ({num_classes} classes)")

    # Update class_names.json registry
    classes_json_path = Path("backend/models/class_names.json")
    classes_dict = {}
    if classes_json_path.exists():
        try:
            with open(classes_json_path, "r") as f:
                classes_dict = json.load(f)
        except Exception:
            classes_dict = {}
    classes_dict["authenticity"] = class_names
    with open(classes_json_path, "w") as f:
        json.dump(classes_dict, f, indent=4)

    # 2. Phase 1: Feature Extraction
    print("\n--- PHASE 1: Feature Extraction (Base Model Frozen) ---")
    model = build_efficientnet_model(
        input_shape=(224, 224, 3),
        num_classes=num_classes,
        learning_rate=initial_lr,
        fine_tune_at=None
    )

    history_head = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs_head,
        class_weight=class_weights,
        verbose=1
    )

    # 3. Phase 2: Fine-Tuning
    history_finetune = None
    if epochs_finetune > 0:
        print("\n--- PHASE 2: Fine-Tuning (Top 20 Layers Unfrozen) ---")
        base_model = None
        for layer in model.layers:
            if "efficientnet" in layer.name:
                base_model = layer
                break

        if base_model:
            base_model.trainable = True
            for layer in base_model.layers:
                if isinstance(layer, tf.keras.layers.BatchNormalization):
                    layer.trainable = False
                elif layer in base_model.layers[:-20]:
                    layer.trainable = False

        loss = "binary_crossentropy" if num_classes == 2 else "sparse_categorical_crossentropy"
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=finetune_lr),
            loss=loss,
            metrics=["accuracy"]
        )

        history_finetune = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs_finetune,
            class_weight=class_weights,
            verbose=1
        )

    # 4. Save Model
    save_path = Path(output_model_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(save_path))
    print(f"[*] Authenticity model saved to: {save_path}")

    # 5. Plot Curves
    graph_path = Path("results/graphs/authenticity_efficientnet_training.png")
    plot_combined_history(history_head, history_finetune, graph_path)
    print("=" * 65)
    print("Stage 2 Authenticity Training Completed Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Authenticity Classifier")
    parser.add_argument("--epochs-head", type=int, default=4)
    parser.add_argument("--epochs-finetune", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--output", type=str, default="backend/models/authenticity_model.keras")
    args = parser.parse_args()

    train_authenticity(
        epochs_head=args.epochs_head,
        epochs_finetune=args.epochs_finetune,
        batch_size=args.batch_size,
        output_model_path=args.output
    )
