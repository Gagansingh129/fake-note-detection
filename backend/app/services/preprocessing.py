"""
NoteGuard AI - Image Preprocessing & Augmentation Pipeline
==========================================================
Standardizes image inputs for Deep Learning inference (224x224 RGB)
and builds controlled augmentation layers for training without distorting
vital currency security features.
"""

from typing import Tuple, Union, Optional
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Sequential

# Standard model input resolution
IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)

def get_training_augmentation_pipeline() -> tf.keras.Sequential:
    """
    Constructs a data augmentation pipeline applied ONLY during training.
    
    Why controlled augmentation?
    - Banknotes have strict horizontal text, specific portrait orientations, and security strips.
    - Aggressive vertical flips or severe shears would create physically impossible notes.
    - We use gentle rotations (±5%), subtle translations, slight zooms, and mild contrast/brightness variations.
    """
    return Sequential([
        layers.RandomRotation(factor=0.05, fill_mode="reflect", name="aug_gentle_rotation"),
        layers.RandomTranslation(height_factor=0.05, width_factor=0.05, fill_mode="reflect", name="aug_translation"),
        layers.RandomZoom(height_factor=(-0.05, 0.05), fill_mode="reflect", name="aug_zoom"),
        layers.RandomContrast(factor=0.1, name="aug_contrast")
    ], name="noteguard_augmentation_pipeline")


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decodes raw uploaded image byte stream into an OpenCV BGR numpy array."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Could not decode image from provided byte stream.")
    return image_bgr


def preprocess_for_inference(
    image_input: Union[str, bytes, np.ndarray],
    target_size: Tuple[int, int] = IMAGE_SIZE,
    model_type: str = "efficientnet",
    auto_crop: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Complete inference preprocessing pipeline:
    1. Reads image (path, bytes, or numpy BGR array).
    2. Auto-detects and crops banknote ROI to eliminate user hands, face, and room background.
    3. Normalizes illumination and micro-contrast using CLAHE.
    4. Converts BGR to RGB and resizes to target dimension (224x224).
    5. Applies model-specific normalization.
    
    Returns:
    - preprocessed_tensor: Batch tensor ready for model.predict() -> shape (1, 224, 224, 3)
    - rgb_display: Standard uint8 RGB image for Grad-CAM overlay -> shape (224, 224, 3)
    - original_bgr: Unmodified original BGR array for quality checks.
    """
    from app.services.image_processing import quality_checker

    # 1. Resolve to OpenCV BGR array
    if isinstance(image_input, str):
        original_bgr = cv2.imread(image_input)
        if original_bgr is None:
            raise FileNotFoundError(f"Image not found at path: {image_input}")
    elif isinstance(image_input, bytes):
        original_bgr = decode_image_bytes(image_input)
    elif isinstance(image_input, np.ndarray):
        original_bgr = image_input.copy()
    else:
        raise TypeError(f"Unsupported image input type: {type(image_input)}")

    # 2. Auto-detect and crop banknote ROI to remove background clutter
    if auto_crop:
        crop_res = quality_checker.detect_and_crop_banknote(original_bgr)
        roi_bgr = crop_res[0]
        was_cropped = crop_res[2]
        processed_bgr = quality_checker.enhance_banknote_contrast(roi_bgr)
    else:
        processed_bgr = original_bgr

    # 3. Convert BGR to RGB
    rgb = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

    # 4. High quality resize to 224x224
    rgb_resized = cv2.resize(rgb, target_size, interpolation=cv2.INTER_AREA)

    # 5. Model-specific normalization
    if model_type.lower() == "efficientnet":
        # EfficientNet expects [0, 255] float input or handles internal scaling,
        # but preprocess_input ensures ImageNet standardization
        tensor_input = tf.keras.applications.efficientnet.preprocess_input(rgb_resized.astype(np.float32))
    elif model_type.lower() == "mobilenet":
        tensor_input = tf.keras.applications.mobilenet_v2.preprocess_input(rgb_resized.astype(np.float32))
    else:
        # Standard custom CNN normalization: scale pixels from [0, 255] to [0.0, 1.0]
        tensor_input = rgb_resized.astype(np.float32) / 255.0

    # Expand dims to create batch dimension (1, 224, 224, 3)
    batch_tensor = np.expand_dims(tensor_input, axis=0)

    return batch_tensor, rgb_resized, original_bgr
