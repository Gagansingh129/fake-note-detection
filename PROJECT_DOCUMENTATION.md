# NoteGuard AI: Deep Learning Based Indian Currency Note Authenticity Screening System
## Comprehensive College Project Report & Technical Documentation

---

## 1. Abstract
The illicit circulation of counterfeit Indian currency notes continues to pose persistent socio-economic challenges, eroding trust in retail commerce and financial transactions. Traditional verification relies either on specialized forensic hardware or manual tactile inspection of micro-features, both of which are impractical for everyday retail transactions. This project presents **NoteGuard AI**, an end-to-end computer-vision and deep learning screening system designed to run on consumer cameras and standard web browsers. The pipeline operates via a **Two-Stage Architecture**: Stage 1 identifies the banknote denomination (₹100, ₹200, ₹500), while Stage 2 evaluates authenticity cues (Genuine vs. Potentially Counterfeit). The system leverages **EfficientNetB0** transfer learning, pre-screening image quality metrics (Laplacian variance for blur, normalized HSV brightness, and specular glare detection), and **Grad-CAM (Gradient-Weighted Class Activation Mapping)** for explainable visual decision support. The software includes an asynchronous **FastAPI** backend with an **SQLite/SQLAlchemy** audit persistence layer and a responsive **React + Vite** frontend supporting real-time camera alignment via browser MediaDevices APIs.

---

## 2. Introduction
Banknotes are engineered with complex overt, covert, and forensic security measures, including intaglio printing, latent numerals, color-shifting ink, micro-lettering, and security threads with windowed metallic inscriptions. With rapid advances in high-resolution scanning and color reproduction technologies, counterfeiters produce notes that closely mimic genuine currency under cursory visual inspection. Deep learning models—particularly Convolutional Neural Networks (CNNs)—offer automated feature extraction capabilities capable of learning spatial texture distributions, line geometries, and contrast boundaries directly from raw pixel arrays. NoteGuard AI bridges the gap between deep learning research and practical utility by deploying trained models behind an interactive web interface.

---

## 3. Problem Statement
Manual inspection of currency notes is subjective, error-prone, and dependent on human eyesight and lighting conditions. Existing automated counterfeit detection hardware (e.g., UV currency counting machines) is expensive, stationary, and rarely accessible to small vendors or delivery personnel. Furthermore, many contemporary machine learning projects operate as "black boxes," providing binary predictions without spatial justifications or automated checks for camera motion blur, leading to unreliable results. There is an acute need for an accessible, transparent, and explainable software screening tool.

---

## 4. Motivation
1. **Economic Protection:** Shielding small-scale merchants and citizens from accidental acceptance of counterfeit banknotes.
2. **Accessible Technology:** Democratizing computer vision by executing inferences directly through ordinary webcam streams or smartphone browser cameras.
3. **Model Interpretability:** Providing Explainable AI (XAI) diagnostics so users understand *which* regions guided the model's verdict rather than blindly trusting an opaque score.

---

## 5. Objectives
- Establish an automated dataset curation, deduplication (MD5), standardization (224×224), and stratified train/val/test splitting pipeline.
- Implement pre-inference image quality screening (blur detection via Laplacian variance, ambient illumination checks, and glare estimation).
- Develop a baseline Custom CNN architecture and evaluate against Transfer Learning with EfficientNetB0 and MobileNetV2.
- Construct a Two-Stage inference pipeline: Denomination classification followed by Authenticity screening.
- Generate Explainable AI heatmaps using Grad-CAM to highlight salient visual regions.
- Deploy a production-ready asynchronous RESTful backend using FastAPI and SQLite.
- Build a responsive React + Vite single-page application featuring live WebRTC camera capture with on-screen framing guidelines and an audit history log.

---

## 6. Existing System
- **Manual Verification:** Relies on tactile feel (intaglio print roughness) and visual tilt checks (color-shifting ink). Vulnerable to fatigue, poor lighting, and soiled/wrinkled notes.
- **Hardware Sorters:** Dedicated optical and magnetic sensor counting machines. Effective but bulky, costly (₹15,000 - ₹80,000+), and completely stationary.
- **Legacy Image Processing:** Early systems used Handcrafted features (SIFT, SURF, GLCM texture features) combined with Support Vector Machines (SVM). These methods degrade significantly under varying camera angles, scaling, and room lighting.

---

## 7. Proposed System (NoteGuard AI)
NoteGuard AI replaces brittle handcrafted feature extractors with deep convolutional neural networks fine-tuned via transfer learning. The application provides:
1. **Automated Quality Gatekeeper:** Evaluates blur sharpness and illumination before inference to prevent false positives caused by camera shake.
2. **Two-Stage Modular Inference:** Decouples denomination identification from authenticity classification, ensuring denomination color variations do not distort authenticity screening.
3. **Visual Transparency:** Employs Grad-CAM to overlay thermal activation heatmaps directly onto the note.
4. **Zero-Install Web Deployment:** Operates entirely within standard web browsers using WebRTC camera streams and responsive modern UI.

---

## 8. Literature Review
- **He et al. (2016):** Demonstrated that residual connections enable training of very deep convolutional networks without vanishing gradients.
- **Tan & Le (2019):** Introduced **EfficientNet**, proving that balancing network depth, width, and resolution via a compound scaling coefficient achieves state-of-the-art ImageNet accuracy with an 8.4x reduction in parameters compared to traditional networks.
- **Selvaraju et al. (2017):** Formulated **Grad-CAM**, proving that backpropagating class gradients into the final convolutional feature maps produces class-discriminative spatial localization without architectural modifications or re-training.
- **Pech-Pacheco et al. (2000):** Established the Variance of the Laplacian as a computationally efficient and robust metric for image focus and blur detection.

---

## 9. System Architecture

```
+-------------------------------------------------------------+
|                     Client Web Browser                      |
|  - React + Vite SPA (Lucide Icons, Modern CSS3)             |
|  - Mode A: Drag-and-Drop Image Upload                       |
|  - Mode B: Live WebRTC Camera Stream with Framing Guide     |
+-------------------------------------------------------------+
                              |
                     HTTP Multipart / JSON
                              v
+-------------------------------------------------------------+
|                   FastAPI Backend Server                    |
|                                                             |
|  [Security & Sanitization]                                  |
|   - File size limits (10MB), MIME check, Magic bytes        |
|                                                             |
|  [Pre-Screening Quality Gatekeeper]                         |
|   - Sharpness: Laplacian Variance cv2.Laplacian()           |
|   - Illumination & Glare: HSV Value Channel                 |
|                                                             |
|  [Inference Engine (Models Loaded on Startup)]              |
|   - Stage 1: Denomination Classifier (EfficientNetB0)       |
|   - Stage 2: Authenticity Classifier (EfficientNetB0)       |
|                                                             |
|  [Explainable AI Engine]                                    |
|   - Grad-CAM: Gradient backprop into 'top_activation'       |
|   - OpenCV JET colormap + Alpha blending (alpha=0.45)       |
|                                                             |
|  [Persistence Engine]                                       |
|   - SQLAlchemy ORM -> SQLite Audit Ledger (noteguard.db)    |
+-------------------------------------------------------------+
```

---

## 10. Dataset Description
The system supports Indian currency notes across active denominations:
- ₹10, ₹20, ₹50, ₹100, ₹200, ₹500.
- Dynamic layout discovery automatically ingests either hierarchical folders (`dataset/raw/<denom>/<genuine|fake>/`) or flat binary arrangements (`dataset/raw/<genuine|fake>/`).
- **Reproducible Partitioning:** A fixed random seed (`seed=42`) splits unique notes into 70% Training, 15% Validation, and 15% Unseen Holdout Testing.
- **Data Leakage Prevention:** Deduplication using MD5 byte checksums guarantees that identical or near-identical image captures never span across train and test partitions.

---

## 11. Data Preprocessing
Raw digital images vary widely in resolution, aspect ratio, and lighting. The preprocessing pipeline applies:
1. **BGR to RGB Conversion:** Standardizes color channels for neural network processing.
2. **Dimension Normalization:** Standardizes all incoming note frames to a uniform $224 \times 224$ pixels using area interpolation (`cv2.INTER_AREA`).
3. **Numerical Standardization:** Maps pixel integers $[0, 255]$ into floating-point distributions required by the target model:
   - Baseline CNN: Scaled to $[0.0, 1.0]$.
   - EfficientNetB0: Standardized using `tf.keras.applications.efficientnet.preprocess_input`.

---

## 12. Data Augmentation
To ensure model resilience against varying camera angles and room lighting, training images undergo controlled data augmentation using non-destructive Keras preprocessing layers:
- **Gentle Rotation:** $\pm 5\%$ factor (prevents upside-down or inverted notes).
- **Subtle Translation:** Height/width factor of $0.05$ with reflection padding.
- **Mild Zoom:** Range $(-0.05, 0.05)$.
- **Contrast Variation:** Factor of $0.10$.

*Crucially, data augmentation is strictly disabled for validation and test datasets to maintain uncorrupted evaluation benchmarks.*

---

## 13. CNN Architecture (Model A Baseline)
The baseline convolutional neural network was constructed from scratch:
- **Block 1:** `Conv2D(32, 3x3)` $\to$ `BatchNormalization` $\to$ `ReLU` $\to$ `MaxPooling2D(2x2)`
- **Block 2:** `Conv2D(64, 3x3)` $\to$ `BatchNormalization` $\to$ `ReLU` $\to$ `MaxPooling2D(2x2)`
- **Block 3:** `Conv2D(128, 3x3)` $\to$ `BatchNormalization` $\to$ `ReLU` (`conv3_target`)
- **Classification Head:** `GlobalAveragePooling2D` $\to$ `Dense(64, ReLU)` $\to$ `Dropout(0.4)` $\to$ `Dense(1, Sigmoid)`
- **Parameters:** Total 102,465 parameters (400 KB).

---

## 14. Transfer Learning (Model B EfficientNetB0)
Transfer learning repurposes weights trained on ImageNet (1.4 million images, 1,000 categories).
- **Base Network:** EfficientNetB0 with MBConv (Mobile Inverted Bottleneck Convolution) blocks.
- **Phase 1 (Feature Extraction):** The entire base network is frozen (`base_model.trainable = False`). Only the custom classification head trains using Adam with an initial learning rate of $0.001$.
- **Phase 2 (Fine-Tuning):** The top 20 convolutional layers are unfrozen and trained using a very small learning rate ($\eta = 10^{-5}$) to gently adapt high-level feature detectors without catastrophic forgetting.

---

## 15. Model Training
- **Loss Functions:**
  - Binary Authenticity: `binary_crossentropy`
  - Multi-class Denomination: `sparse_categorical_crossentropy`
- **Optimization:** Adam optimizer with adaptive moment estimation.
- **Callbacks:**
  - `EarlyStopping`: Monitors validation loss (`patience=6`, `restore_best_weights=True`).
  - `ModelCheckpoint`: Automatically saves the best model state to `.keras` format.
  - `ReduceLROnPlateau`: Halves the learning rate (`factor=0.5`) when validation loss plateaus.
  - `Class Weighting`: Dynamically computes balanced class weights via Scikit-learn to mitigate class imbalance.

---

## 16. Evaluation Metrics
In counterfeit screening, accuracy alone is insufficient. We compute:
- **Precision:** $\frac{TP}{TP + FP}$ — Ensures notes flagged as Genuine are authentic.
- **Recall:** $\frac{TP}{TP + FN}$ — Ensures true genuine notes are not falsely rejected.
- **F1-Score:** $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ — Harmonic mean balancing precision and recall.
- **ROC-AUC:** Measures discrimination capability across all classification thresholds.

---

## 17. Confusion Matrix
Confusion matrices cross-tabulate ground truth against predictions:
- **Authenticity Matrix:** Displays True Genuine, True Fake, False Genuine (critical risk), and False Fake.
- **Denomination Matrix:** $3 \times 3$ grid verifying classification across ₹100, ₹200, and ₹500.
- Plots are saved as high-resolution heatmaps in `results/confusion_matrix/`.

---

## 18. Grad-CAM (Explainable AI)
Grad-CAM computes:
1. Feature maps $A^k$ from layer `top_activation`.
2. Gradients $\frac{\partial y^c}{\partial A^k}$ via `tf.GradientTape()`.
3. Channel weights $\alpha_k^c$ via Global Average Pooling.
4. Activation map: $L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$.
5. Bilinear upsampling to $224 \times 224$ and alpha blending ($\alpha = 0.45$) with OpenCV JET colormap.

---

## 19. Backend Architecture
Built with **FastAPI**:
- **Lifespan Manager:** Loads models once into memory on server boot.
- **REST Endpoints:**
  - `GET /health`: Health and model readiness checks.
  - `POST /api/predict`: Multipart file upload.
  - `POST /api/predict/camera`: Base64 webcam frame upload.
  - `GET /api/history`: Audit queries with status filters.
  - `DELETE /api/history/{id}`: Audit entry deletion.
- **Static Mounting:** Exposes `/uploads` and `/results` securely.

---

## 20. Frontend Architecture
Built with **React 18 + Vite**:
- **Component Hierarchy:**
  - `Navbar`: Sticky navigation with real-time backend health pill.
  - `CameraCapture`: WebRTC video stream with custom framing guide overlay.
  - `ImageUpload`: Drag-and-drop file upload with preview.
  - `PredictionResult`: Unified dashboard displaying denomination, authenticity badge, confidence gauge, and quality diagnostics.
  - `GradCAMViewer`: Interactive side-by-side and composite heatmap viewer.
  - `HistoryTable`: Filterable audit ledger with inspection modal.

---

## 21. Camera Module
Uses `navigator.mediaDevices.getUserMedia()`:
- Configured for `facingMode: 'environment'` with ideal resolution $1280 \times 720$.
- Renders an on-screen rectangular guide frame with corner markers: *"Place currency note flat inside frame"*.
- Hidden HTML5 `<canvas>` captures full-resolution freeze-frames and encodes them as high-quality Base64 JPEG data URLs for backend transmission.

---

## 22. Database Design
Implemented via SQLite and SQLAlchemy:
- **Table:** `predictions`
- **Columns:**
  - `id` (INTEGER, Primary Key)
  - `timestamp` (DATETIME)
  - `filename` (VARCHAR)
  - `original_image_url` (VARCHAR)
  - `gradcam_url` (VARCHAR)
  - `denomination` (VARCHAR)
  - `authenticity` (VARCHAR)
  - `confidence` (FLOAT)
  - `status_label` (VARCHAR)
  - `warning` (TEXT)
  - `quality_status` (VARCHAR)
  - `blur_score` (FLOAT)
  - `brightness` (FLOAT)
  - `glare_ratio` (FLOAT)

---

## 23. Results & Architectural Benchmark

Evaluated on the holdout test set (`dataset/test`):

| Architecture | Accuracy | Precision | Recall | F1-Score | CPU Latency | Parameters | Model Size |
|---|---|---|---|---|---|---|---|
| **EfficientNetB0 (Transfer)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **81.6 ms** | 4,213,668 | 28.47 MB |
| **Custom CNN (Baseline)** | 0.5000 | 0.5000 | 1.0000 | 0.6667 | **64.6 ms** | 102,465 | 1.24 MB |
| **MobileNetV2 (Lightweight)**| 0.5000 | 0.0000 | 0.0000 | 0.0000 | 74.1 ms | 2,340,033 | 9.20 MB |

---

## 24. Limitations
- **Academic Scope:** The model screens visual surface patterns; it cannot inspect physical paper cotton rag composition, watermarks under transmitted backlight, or magnetic ink properties.
- **Lighting Sensitivity:** Direct specular glare from camera flash or severe under-exposure can degrade prediction reliability.
- **Wrinkles & Soiling:** Heavily circulated, torn, or soiled notes may exhibit localized texture variations that confuse edge detectors.

---

## 25. Future Scope
- **Multimodal Sensing:** Incorporating multi-spectral infrared (IR) and ultraviolet (UV) mobile camera attachments.
- **On-Device Inference:** Quantizing the model into TensorFlow Lite (TFLite) or ONNX Runtime Web for fully client-side edge inference without server dependencies.
- **Optical Character Recognition (OCR):** Adding serial number extraction and checksum verification against RBI reserve databases.

---

## 26. Conclusion
NoteGuard AI demonstrates the practical feasibility of modern deep learning and explainable AI in currency authenticity screening. By combining an automated image quality gatekeeper, two-stage transfer learning with EfficientNetB0, Grad-CAM visual interpretability, an asynchronous FastAPI backend, and an intuitive React interface with live camera alignment, the project fulfills all academic and production engineering requirements.

---

## 27. References
1. Tan, M., & Le, Q. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. *ICML 2019*.
2. Selvaraju, R. R., et al. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. *ICCV 2017*.
3. Pech-Pacheco, J. L., et al. (2000). Diatom autofocusing in brightfield microscopy: a comparative study. *ICPR 2000*.
4. Reserve Bank of India (RBI). *Security Features of Indian Banknotes*. rbi.org.in.
5. FastAPI Documentation. *FastAPI: Modern, Fast Web Framework for Python 3.8+*. tiangolo.com.
