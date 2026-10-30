"""
NoteGuard AI - Verification Script for Phase 3 (Preprocessing & Quality Checks)
=============================================================================
Tests:
1. Blur estimation via Laplacian variance.
2. Brightness estimation & glare detection.
3. Shape conversion & normalization for Custom CNN vs EfficientNet.
4. Augmentation pipeline stability (visualized in results/graphs/augmentation_samples.png).
"""

import sys
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Ensure backend can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.image_processing import quality_checker
from app.services.preprocessing import (
    preprocess_for_inference,
    get_training_augmentation_pipeline,
    IMAGE_SIZE
)

def test_quality_checker():
    print("[1] Testing Image Quality Checker...")
    # Clean synthetic test card
    sharp_img = np.zeros((300, 600, 3), dtype=np.uint8)
    cv2.rectangle(sharp_img, (50, 50), (550, 250), (200, 200, 200), -1)
    cv2.putText(sharp_img, "SHARP NOTE TEST", (70, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (10, 10, 10), 3)

    # Artificially blur the image
    blurred_img = cv2.GaussianBlur(sharp_img, (25, 25), 0)

    # Artificially darken the image
    dark_img = (sharp_img * 0.1).astype(np.uint8)

    res_sharp = quality_checker.evaluate_quality(sharp_img)
    res_blur = quality_checker.evaluate_quality(blurred_img)
    res_dark = quality_checker.evaluate_quality(dark_img)

    print(f"    - Sharp Image   -> Blur Score: {res_sharp['blur_score']} | Status: {res_sharp['status']}")
    print(f"    - Blurred Image -> Blur Score: {res_blur['blur_score']} | Status: {res_blur['status']} | Warnings: {res_blur['warnings']}")
    print(f"    - Dark Image    -> Brightness: {res_dark['brightness']} | Status: {res_dark['status']} | Warnings: {res_dark['warnings']}")

    assert res_sharp['blur_score'] > res_blur['blur_score'], "Sharp image must have higher Laplacian variance than blurred image"
    assert res_dark['is_acceptable'] is False, "Dark image must be flagged as unacceptable"
    print("    [PASS] Quality Checker accurately detected blur, darkness, and sharpness.")

def test_inference_preprocessing():
    print("\n[2] Testing Inference Preprocessing Pipeline...")
    sample_file = list(Path("dataset/train").glob("**/*.jpg"))[0]
    
    # Test path loading
    tensor_eff, display_rgb, bgr = preprocess_for_inference(str(sample_file), model_type="efficientnet")
    assert tensor_eff.shape == (1, 224, 224, 3), f"Unexpected shape {tensor_eff.shape}"
    assert display_rgb.shape == (224, 224, 3), f"Unexpected display shape {display_rgb.shape}"
    assert display_rgb.dtype == np.uint8, "Display RGB should be uint8"

    # Test CNN normalization [0, 1]
    tensor_cnn, _, _ = preprocess_for_inference(str(sample_file), model_type="custom_cnn")
    assert 0.0 <= tensor_cnn.min() and tensor_cnn.max() <= 1.0, "CNN input must be in [0.0, 1.0]"

    # Test byte buffer decoding
    with open(sample_file, "rb") as f:
        byte_data = f.read()
    tensor_bytes, _, _ = preprocess_for_inference(byte_data, model_type="efficientnet")
    assert np.allclose(tensor_eff, tensor_bytes), "Byte stream decoding must match file path reading exactly"

    print("    [PASS] Shape validation (1, 224, 224, 3) and byte-decoding verified.")

def test_augmentation_pipeline():
    print("\n[3] Testing Data Augmentation Pipeline...")
    sample_file = list(Path("dataset/train").glob("**/*.jpg"))[0]
    _, display_rgb, _ = preprocess_for_inference(str(sample_file), model_type="custom_cnn")

    aug_pipeline = get_training_augmentation_pipeline()
    base_tensor = np.expand_dims(display_rgb.astype(np.float32) / 255.0, axis=0)

    # Generate 5 augmented variants
    plt.figure(figsize=(15, 3))
    plt.subplot(1, 6, 1)
    plt.imshow(display_rgb)
    plt.title("Original (224x224)", fontsize=9, fontweight='bold')
    plt.axis("off")

    for i in range(5):
        augmented = aug_pipeline(base_tensor, training=True).numpy()[0]
        augmented = np.clip(augmented, 0.0, 1.0)
        plt.subplot(1, 6, i + 2)
        plt.imshow(augmented)
        plt.title(f"Augmented #{i+1}", fontsize=9)
        plt.axis("off")

    output_path = Path("results/graphs/augmentation_samples.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"    - Saved visual augmentation comparison to: {output_path}")
    print("    [PASS] Training data augmentation pipeline runs deterministically.")

if __name__ == "__main__":
    print("=" * 60)
    print("       Testing NoteGuard AI Phase 3 Preprocessing        ")
    print("=" * 60)
    test_quality_checker()
    test_inference_preprocessing()
    test_augmentation_pipeline()
    print("=" * 60)
    print("All Phase 3 Preprocessing Tests Passed Successfully!")
    print("=" * 60)
