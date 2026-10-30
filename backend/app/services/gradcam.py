"""
NoteGuard AI - Grad-CAM (Gradient-Weighted Class Activation Mapping) Service
============================================================================
Provides Explainable AI (XAI) diagnostics for currency screening models.
Highlights spatial regions of banknotes that influenced the model's prediction
without claiming legal or forensic certainty.
"""

from pathlib import Path
from typing import Tuple, Optional, Union
import cv2
import numpy as np
import tensorflow as tf


def find_target_conv_layer(model: tf.keras.Model, layer_name: Optional[str] = None):
    """
    Automatically detects the target convolutional layer for Grad-CAM.
    Supports both direct CNNs and nested Transfer Learning models (EfficientNet).
    """
    if layer_name:
        try:
            return model.get_layer(layer_name), model, False
        except ValueError:
            pass
        for layer in model.layers:
            if hasattr(layer, "layers"):
                try:
                    return layer.get_layer(layer_name), layer, True
                except ValueError:
                    pass
        raise ValueError(f"Requested layer '{layer_name}' not found in model hierarchy.")

    # 1. Search inside nested sub-models (e.g. EfficientNet)
    for layer in reversed(model.layers):
        if hasattr(layer, "layers"):
            for sub_layer in reversed(layer.layers):
                name = sub_layer.name.lower()
                typename = type(sub_layer).__name__.lower()
                if name in ["top_activation", "top_conv"] or "conv2d" in typename or ("conv" in name and "bn" not in name):
                    return sub_layer, layer, True

    # 2. Search direct model layers
    for layer in reversed(model.layers):
        name = layer.name.lower()
        typename = type(layer).__name__.lower()
        if "conv2d" in typename or "target" in name or ("conv" in name and "bn" not in name):
            return layer, model, False

    raise RuntimeError("Could not automatically locate a convolutional layer for Grad-CAM.")


def compute_gradcam_heatmap(
    model: tf.keras.Model,
    img_tensor: np.ndarray,
    class_idx: Optional[int] = None,
    target_layer_name: Optional[str] = None
) -> np.ndarray:
    """
    Computes normalized Grad-CAM heatmap for the given input image tensor.
    - img_tensor: Preprocessed batch tensor (1, 224, 224, 3)
    - class_idx: Target class index to explain (defaults to model's predicted class)
    """
    target_layer, sub_model, is_nested = find_target_conv_layer(model, target_layer_name)

    if is_nested:
        # Transfer Learning Model (e.g. EfficientNet)
        feature_extractor = tf.keras.Model(sub_model.inputs, [target_layer.output, sub_model.output])
        
        # Build head submodel from model layers following sub_model
        head_input = tf.keras.Input(shape=sub_model.output_shape[1:])
        x = head_input
        # Find index of sub_model in top model
        sub_idx = model.layers.index(sub_model)
        for layer in model.layers[sub_idx + 1:]:
            x = layer(x)
        head_model = tf.keras.Model(head_input, x)

        with tf.GradientTape() as tape:
            conv_outputs, base_outputs = feature_extractor(img_tensor)
            tape.watch(conv_outputs)
            predictions = head_model(base_outputs)
            
            if class_idx is None:
                if predictions.shape[-1] == 1:
                    class_idx = 0
                else:
                    class_idx = int(tf.argmax(predictions[0]))

            if predictions.shape[-1] == 1:
                loss = predictions[0, 0] if class_idx == 1 else (1.0 - predictions[0, 0])
            else:
                loss = predictions[:, class_idx]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = conv_outputs[0] @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

    else:
        # Direct Custom CNN
        grad_model = tf.keras.Model(model.inputs, [target_layer.output, model.output])
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_tensor)
            if class_idx is None:
                if predictions.shape[-1] == 1:
                    class_idx = 0
                else:
                    class_idx = int(tf.argmax(predictions[0]))

            if predictions.shape[-1] == 1:
                loss = predictions[0, 0] if class_idx == 1 else (1.0 - predictions[0, 0])
            else:
                loss = predictions[:, class_idx]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = conv_outputs[0] @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

    # Apply ReLU: only positive contributions highlight regions of interest
    heatmap = tf.maximum(heatmap, 0.0)
    max_val = tf.math.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val
    return heatmap.numpy()


def overlay_heatmap_on_image(
    original_rgb: np.ndarray,
    heatmap: np.ndarray,
    alpha: float = 0.45,
    colormap: int = cv2.COLORMAP_JET
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Overlays 2D Grad-CAM heatmap onto original RGB image.
    Returns:
    - heatmap_resized_rgb: Colorized 224x224 heatmap
    - overlay_rgb: Blended 224x224 RGB image
    - side_by_side: 3-panel composite (Original | Heatmap | Overlay)
    """
    h, w = original_rgb.shape[:2]
    # Resize heatmap to match image resolution
    heatmap_resized = cv2.resize(heatmap, (w, h), interpolation=cv2.INTER_CUBIC)
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap_resized, 0.0, 1.0))
    
    # Apply JET colormap (BGR output from OpenCV)
    heatmap_color_bgr = cv2.applyColorMap(heatmap_uint8, colormap)
    heatmap_color_rgb = cv2.cvtColor(heatmap_color_bgr, cv2.COLOR_BGR2RGB)

    # Alpha blend: (1 - alpha) * original + alpha * heatmap
    overlay = cv2.addWeighted(original_rgb, 1.0 - alpha, heatmap_color_rgb, alpha, 0)

    # Build side-by-side composite
    composite = np.zeros((h, w * 3 + 40, 3), dtype=np.uint8)
    composite[:, :w] = original_rgb
    composite[:, w + 20:2 * w + 20] = heatmap_color_rgb
    composite[:, 2 * w + 40:] = overlay

    return heatmap_color_rgb, overlay, composite
