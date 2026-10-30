"""
NoteGuard AI - Grad-CAM Visualizer Script
=========================================
Generates side-by-side Explainable AI (XAI) figures for Indian currency notes.
Produces:
1. Original Note Image (224x224 RGB)
2. Grad-CAM Activation Heatmap
3. Blended Diagnostic Overlay
"""

import sys
import argparse
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from backend.app.services.preprocessing import preprocess_for_inference
from backend.app.services.gradcam import compute_gradcam_heatmap, overlay_heatmap_on_image


def generate_gradcam_figures(
    model_path: str = "backend/models/authenticity_model.keras",
    model_type: str = "efficientnet",
    output_dir: str = "results/gradcam"
):
    print("=" * 65)
    print("       NoteGuard AI - Grad-CAM Heatmap Diagnostic Suite       ")
    print("=" * 65)

    model = tf.keras.models.load_model(model_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Collect sample test images
    test_images = list(Path("dataset/test").glob("**/*.jpg"))
    if not test_images:
        print("[!] No test images found in dataset/test.")
        return

    # Select representative samples (genuine and fake)
    samples_to_test = []
    for p in test_images:
        if "genuine" in str(p).lower() and not any("genuine" in s[1] for s in samples_to_test):
            samples_to_test.append((p, "genuine"))
        elif "fake" in str(p).lower() and not any("fake" in s[1] for s in samples_to_test):
            samples_to_test.append((p, "fake"))
        if len(samples_to_test) >= 2:
            break

    if not samples_to_test:
        samples_to_test = [(test_images[0], "sample")]

    for img_path, label_tag in samples_to_test:
        print(f"\n[*] Processing sample: {img_path.name} (True class: {label_tag})")
        
        # 1. Preprocess
        tensor_input, rgb_display, _ = preprocess_for_inference(str(img_path), model_type=model_type)

        # 2. Predict
        preds = model.predict(tensor_input, verbose=0)
        confidence = float(preds[0, 0]) if preds.shape[-1] == 1 else float(np.max(preds[0]))
        pred_label = "Genuine" if (preds.shape[-1] == 1 and preds[0, 0] >= 0.5) or (preds.shape[-1] > 1 and np.argmax(preds[0]) == 1) else "Fake"
        
        # 3. Compute Grad-CAM
        heatmap = compute_gradcam_heatmap(model, tensor_input)
        heatmap_rgb, overlay, _ = overlay_heatmap_on_image(rgb_display, heatmap, alpha=0.45)

        # 4. Create Matplotlib 3-panel figure
        fig, axes = plt.subplots(1, 3, figsize=(14, 5))
        
        # Panel 1: Original
        axes[0].imshow(rgb_display)
        axes[0].set_title(f"Original Note (224x224)\nGround Truth: {label_tag.upper()}", fontsize=11, fontweight="bold")
        axes[0].axis("off")

        # Panel 2: Heatmap
        axes[1].imshow(heatmap_rgb)
        axes[1].set_title("Grad-CAM Activation\n(Salient Feature Regions)", fontsize=11, fontweight="bold")
        axes[1].axis("off")

        # Panel 3: Overlay
        axes[2].imshow(overlay)
        axes[2].set_title(f"Diagnostic Overlay\nPrediction: {pred_label} ({confidence*100:.1f}%)", fontsize=11, fontweight="bold")
        axes[2].axis("off")

        plt.suptitle(
            "NoteGuard AI - Visual Decision Support (Grad-CAM Explainability)\n"
            "Academic Screening Visualization - Not a Forensic Certificate",
            fontsize=12,
            fontweight="bold",
            y=0.98
        )
        plt.tight_layout()

        fig_save_path = output_path / f"gradcam_{label_tag}_{img_path.stem}.png"
        plt.savefig(fig_save_path, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"    -> Saved Grad-CAM figure to: {fig_save_path}")

    print("\n" + "=" * 65)
    print("Grad-CAM Diagnostic Visualizations Generated Successfully!")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Grad-CAM Visualizations")
    parser.add_argument("--model", type=str, default="backend/models/authenticity_model.keras")
    parser.add_argument("--type", type=str, default="efficientnet")
    parser.add_argument("--output", type=str, default="results/gradcam")
    args = parser.parse_args()

    generate_gradcam_figures(model_path=args.model, model_type=args.type, output_dir=args.output)
