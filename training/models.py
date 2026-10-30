"""
NoteGuard AI - Deep Learning Model Architectures
================================================
Implements:
1. Model A: Custom Baseline CNN from scratch.
2. Model B: Transfer Learning with EfficientNetB0 (Feature extraction + Fine tuning).
3. Model C: MobileNetV2 for lightweight mobile comparison.
"""

from typing import Tuple, Optional
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

def build_baseline_cnn(
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    num_classes: int = 2,
    learning_rate: float = 0.001
) -> tf.keras.Model:
    """
    Model A - Baseline CNN from Scratch
    
    Architecture:
    Input (224, 224, 3)
      -> Conv2D(32, 3x3, same) -> BatchNorm -> ReLU -> MaxPool(2x2)
      -> Conv2D(64, 3x3, same) -> BatchNorm -> ReLU -> MaxPool(2x2)
      -> Conv2D(128, 3x3, same) -> BatchNorm -> ReLU
      -> GlobalAveragePooling2D
      -> Dense(64, ReLU) -> Dropout(0.4)
      -> Output (Dense num_classes)
    """
    inputs = layers.Input(shape=input_shape, name="input_image")
    
    # Block 1
    x = layers.Conv2D(32, (3, 3), padding="same", name="conv1")(inputs)
    x = layers.BatchNormalization(name="bn1")(x)
    x = layers.Activation("relu", name="relu1")(x)
    x = layers.MaxPooling2D((2, 2), name="pool1")(x)

    # Block 2
    x = layers.Conv2D(64, (3, 3), padding="same", name="conv2")(x)
    x = layers.BatchNormalization(name="bn2")(x)
    x = layers.Activation("relu", name="relu2")(x)
    x = layers.MaxPooling2D((2, 2), name="pool2")(x)

    # Block 3 (Target conv layer for Grad-CAM)
    x = layers.Conv2D(128, (3, 3), padding="same", name="conv3_target")(x)
    x = layers.BatchNormalization(name="bn3")(x)
    x = layers.Activation("relu", name="relu3")(x)

    # Classification Head
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dense(64, activation="relu", name="dense_features")(x)
    x = layers.Dropout(0.4, name="dropout")(x)

    if num_classes == 2:
        outputs = layers.Dense(1, activation="sigmoid", name="predictions")(x)
        loss = "binary_crossentropy"
        metrics = ["accuracy"]
    else:
        outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
        loss = "sparse_categorical_crossentropy"
        metrics = ["accuracy"]

    model = models.Model(inputs=inputs, outputs=outputs, name="noteguard_baseline_cnn")

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def build_efficientnet_model(
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    num_classes: int = 2,
    learning_rate: float = 0.001,
    fine_tune_at: Optional[int] = None
) -> tf.keras.Model:
    """
    Model B - Transfer Learning via EfficientNetB0
    """
    base_model = tf.keras.applications.EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )

    if fine_tune_at is None:
        # Phase 1: Feature Extraction (Freeze base model completely)
        base_model.trainable = False
    else:
        # Phase 2: Fine-Tuning (Unfreeze upper layers from fine_tune_at index)
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

    inputs = layers.Input(shape=input_shape, name="input_image")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dropout(0.3, name="head_dropout")(x)
    x = layers.Dense(128, activation="relu", name="head_dense")(x)
    x = layers.Dropout(0.2, name="head_dropout2")(x)

    if num_classes == 2:
        outputs = layers.Dense(1, activation="sigmoid", name="predictions")(x)
        loss = "binary_crossentropy"
    else:
        outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
        loss = "sparse_categorical_crossentropy"

    model = models.Model(inputs=inputs, outputs=outputs, name="noteguard_efficientnet_b0")
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])
    return model


def build_mobilenet_model(
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    num_classes: int = 2,
    learning_rate: float = 0.001
) -> tf.keras.Model:
    """
    Model C - MobileNetV2 for lightweight device inference
    """
    base_model = tf.keras.applications.MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )
    base_model.trainable = False

    inputs = layers.Input(shape=input_shape, name="input_image")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dropout(0.3, name="head_dropout")(x)
    x = layers.Dense(64, activation="relu", name="head_dense")(x)

    if num_classes == 2:
        outputs = layers.Dense(1, activation="sigmoid", name="predictions")(x)
        loss = "binary_crossentropy"
    else:
        outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
        loss = "sparse_categorical_crossentropy"

    model = models.Model(inputs=inputs, outputs=outputs, name="noteguard_mobilenet_v2")
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])
    return model
