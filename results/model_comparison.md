# NoteGuard AI - Architectural Model Comparison

| Architecture | Accuracy | Precision | Recall | F1-Score | Latency (CPU) | Parameters | Model Size |
|---|---|---|---|---|---|---|---|
| **EfficientNetB0 (Transfer)** | 0.8552 | 0.8971 | 0.8714 | 0.8841 | 108.5 ms | 4,213,668 | 28.4 MB |
| **Custom CNN (Baseline)** | 0.3665 | 0.0000 | 0.0000 | 0.0000 | 71.7 ms | 102,465 | 1.24 MB |
| **MobileNetV2 (Lightweight)** | 0.6335 | 0.6335 | 1.0000 | 0.7756 | 83.4 ms | 2,340,033 | 9.2 MB |
