"""
NoteGuard AI - Baseline CNN Training Script
===========================================
Trains the custom convolutional neural network (Model A) from scratch.
Logs training progress, plots accuracy/loss curves, and persists model weights.
"""

import sys
import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf

# Include project paths
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from training.models import build_baseline_cnn
from training.dataset_loader import load_dataset_tf


def plot_training_curves(history, output_path: Path, title_prefix: str = "Baseline CNN"):
    """Generates and saves professional 2-panel training history curves."""
    acc = history.history.get("accuracy", [])
    val_acc = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    # Panel 1: Accuracy Curve
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, "b-o", label="Training Accuracy", linewidth=2)
    plt.plot(epochs, val_acc, "g--s", label="Validation Accuracy", linewidth=2)
    plt.title(f"{title_prefix} - Accuracy Progression", fontsize=11, fontweight="bold")
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Accuracy", fontsize=10)
    plt.ylim([0, 1.05])
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Panel 2: Loss Curve
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, "b-o", label="Training Loss", linewidth=2)
    plt.plot(epochs, val_loss, "r--s", label="Validation Loss", linewidth=2)
    plt.title(f"{title_prefix} - Loss Progression", fontsize=11, fontweight="bold")
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Loss", fontsize=10)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"[*] Training curve saved to: {output_path}")


def train_baseline(
    train_dir: str = "dataset/train",
    val_dir: str = "dataset/validation",
    task: str = "authenticity",
    epochs: int = 15,
    batch_size: int = 16,
    lr: float = 0.001,
    output_model_path: str = "backend/models/baseline_cnn.keras"
):
    print("=" * 65)
    print(f"     NoteGuard AI - Training Model A (Baseline CNN) [{task.upper()}]     ")
    print("=" * 65)

    # 1. Load Data
    train_ds, class_names, class_weights = load_dataset_tf(
        train_dir, task=task, batch_size=batch_size, is_training=True, normalization="rescaling"
    )
    val_ds, _, _ = load_dataset_tf(
        val_dir, task=task, batch_size=batch_size, is_training=False, normalization="rescaling"
    )

    num_classes = len(class_names)
    print(f"[*] Detected classes: {class_names} ({num_classes} classes)")
    if class_weights:
        print(f"[*] Computed class weights: {class_weights}")

    # Save class names mapping
    classes_json = Path("backend/models/class_names.json")
    classes_json.parent.mkdir(parents=True, exist_ok=True)
    with open(classes_json, "w") as f:
        json.dump({task: class_names}, f, indent=4)
    print(f"[*] Class names registry updated at: {classes_json}")

    # 2. Build Model
    model = build_baseline_cnn(input_shape=(224, 224, 3), num_classes=num_classes, learning_rate=lr)
    model.summary()

    # 3. Callbacks
    save_path = Path(output_model_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(save_path),
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    # 4. Train Model
    print("\n[*] Starting training loop...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )

    # 5. Plot Curves
    graph_path = Path(f"results/graphs/baseline_cnn_{task}_training.png")
    plot_training_curves(history, graph_path, title_prefix=f"Baseline CNN ({task.capitalize()})")

    # 6. Ensure model is saved
    if not save_path.exists():
        model.save(str(save_path))
    print(f"[*] Model successfully saved to: {save_path}")

    # Final Epoch Summary
    final_epoch = len(history.history["loss"])
    print("\n" + "=" * 65)
    print("Baseline CNN Training Summary:")
    print(f"  Total Epochs Completed: {final_epoch}")
    print(f"  Final Training Loss:    {history.history['loss'][-1]:.4f}")
    print(f"  Final Training Accuracy:{history.history['accuracy'][-1]:.4f}")
    print(f"  Final Val Loss:         {history.history['val_loss'][-1]:.4f}")
    print(f"  Final Val Accuracy:     {history.history['val_accuracy'][-1]:.4f}")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Baseline CNN for NoteGuard AI")
    parser.add_argument("--train-dir", type=str, default="dataset/train")
    parser.add_argument("--val-dir", type=str, default="dataset/validation")
    parser.add_argument("--task", type=str, default="authenticity", choices=["authenticity", "denomination"])
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--output", type=str, default="backend/models/baseline_cnn.keras")
    args = parser.parse_args()

    train_baseline(
        train_dir=args.train_dir,
        val_dir=args.val_dir,
        task=args.task,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        output_model_path=args.output
    )
