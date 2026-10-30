"""
Generates the 5 college project Jupyter notebooks for NoteGuard AI.
"""

import json
from pathlib import Path

def create_notebook(cells, filename):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.9"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    path = Path("notebooks") / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"[*] Generated notebook: {path}")

# Notebook 1: Dataset Exploration
nb1_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# NoteGuard AI - Notebook 01: Dataset Exploration & Integrity Analysis\n",
            "\n",
            "### Objectives:\n",
            "1. Inspect raw Indian currency note dataset hierarchy.\n",
            "2. Verify image dimensions, file formats, and channel configurations.\n",
            "3. Analyze class balance between Genuine and Fake samples across denominations (₹100, ₹200, ₹500).\n",
            "4. Detect potential data leakage vectors and compute MD5 deduplication hashes."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import glob\n",
            "from pathlib import Path\n",
            "import cv2\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "RAW_DIR = Path('../dataset/raw')\n",
            "print(f'Raw dataset directory: {RAW_DIR.resolve()}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. File Discovery & Extension Verification"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "samples = []\n",
            "for p in RAW_DIR.glob('**/*.*'):\n",
            "    if p.is_file() and p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:\n",
            "        parts = [part.lower() for part in p.parts]\n",
            "        auth = 'genuine' if 'genuine' in parts else 'fake'\n",
            "        denom = [d for d in ['100', '200', '500', '2000'] if d in parts]\n",
            "        samples.append({\n",
            "            'file': str(p),\n",
            "            'denomination': denom[0] if denom else 'unknown',\n",
            "            'authenticity': auth,\n",
            "            'size_kb': round(p.stat().st_size / 1024, 2)\n",
            "        })\n",
            "\n",
            "df = pd.DataFrame(samples)\n",
            "print(f'Total raw samples discovered: {len(df)}')\n",
            "df.head()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2. Class Distribution Visualizations"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "if not df.empty:\n",
            "    plt.figure(figsize=(10, 4))\n",
            "    plt.subplot(1, 2, 1)\n",
            "    df['authenticity'].value_counts().plot(kind='bar', color=['#10b981', '#ef4444'])\n",
            "    plt.title('Distribution by Authenticity')\n",
            "    plt.ylabel('Count')\n",
            "\n",
            "    plt.subplot(1, 2, 2)\n",
            "    df['denomination'].value_counts().plot(kind='bar', color=['#3b82f6', '#8b5cf6', '#ec4899'])\n",
            "    plt.title('Distribution by Denomination')\n",
            "    plt.ylabel('Count')\n",
            "    plt.tight_layout()\n",
            "    plt.show()"
        ]
    }
]

# Notebook 2: Preprocessing
nb2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# NoteGuard AI - Notebook 02: Image Preprocessing & Quality Screening\n",
            "\n",
            "### Objectives:\n",
            "1. Implement Laplacian variance blur detection to flag camera shake.\n",
            "2. Estimate ambient brightness and specular glare using HSV color space.\n",
            "3. Perform standardized 224x224 RGB image normalization.\n",
            "4. Build controlled data augmentation pipelines (rotation, zoom, contrast)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import sys\n",
            "from pathlib import Path\n",
            "sys.path.append(str(Path('..').resolve() / 'backend'))\n",
            "\n",
            "import cv2\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "from app.services.image_processing import quality_checker\n",
            "from app.services.preprocessing import preprocess_for_inference, get_training_augmentation_pipeline"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 1. Testing Sharpness & Blur via Laplacian Variance"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sample_path = list(Path('../dataset/train').glob('**/*.jpg'))[0]\n",
            "img_bgr = cv2.imread(str(sample_path))\n",
            "\n",
            "# Evaluate pristine vs blurred image\n",
            "sharp_score = quality_checker.calculate_blur(img_bgr)\n",
            "blurred = cv2.GaussianBlur(img_bgr, (21, 21), 0)\n",
            "blurred_score = quality_checker.calculate_blur(blurred)\n",
            "\n",
            "print(f'Sharp Note Laplacian Variance: {sharp_score}')\n",
            "print(f'Blurred Note Laplacian Variance: {blurred_score}')"
        ]
    }
]

# Notebook 3: Model Training
nb3_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# NoteGuard AI - Notebook 03: Deep Learning Model Training\n",
            "\n",
            "### Architectures Explored:\n",
            "1. **Model A:** Custom Baseline CNN (Conv2D -> BatchNorm -> ReLU -> GAP -> Dense).\n",
            "2. **Model B:** EfficientNetB0 Transfer Learning with ImageNet weights.\n",
            "3. **Two-Phase Training:** Feature Extraction (Frozen Base) followed by Fine-Tuning (Unfrozen top layers, LR=1e-5)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import tensorflow as tf\n",
            "from training.models import build_baseline_cnn, build_efficientnet_model\n",
            "from training.dataset_loader import load_dataset_tf\n",
            "\n",
            "# Verify TensorFlow installation\n",
            "print('TensorFlow Version:', tf.__version__)"
        ]
    }
]

# Notebook 4: Evaluation
nb4_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# NoteGuard AI - Notebook 04: Evaluation Metrics & Confusion Matrix\n",
            "\n",
            "### Key Topics:\n",
            "1. Holdout test evaluation on unseen test dataset.\n",
            "2. Precision, Recall, F1-score, and Confusion Matrices.\n",
            "3. Why Accuracy can be misleading in fraud and counterfeit detection.\n",
            "4. Empirical model comparison table (Baseline CNN vs EfficientNetB0 vs MobileNetV2)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import json\n",
            "\n",
            "with open('../results/model_comparison.json', 'r') as f:\n",
            "    comparison = json.load(f)\n",
            "\n",
            "pd.DataFrame(comparison)"
        ]
    }
]

# Notebook 5: Grad-CAM
nb5_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# NoteGuard AI - Notebook 05: Explainable AI with Grad-CAM\n",
            "\n",
            "### Objectives:\n",
            "1. Compute Class Activation Maps using gradients from the deepest convolutional layer.\n",
            "2. Colorize heatmaps using OpenCV Jet colormap.\n",
            "3. Alpha blend heatmaps onto input currency notes.\n",
            "4. Understand the distinction between AI decision support and legal forensic proof."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from backend.app.services.gradcam import compute_gradcam_heatmap, overlay_heatmap_on_image\n",
            "from backend.app.services.preprocessing import preprocess_for_inference\n",
            "import tensorflow as tf\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "model = tf.keras.models.load_model('../backend/models/authenticity_model.keras')\n",
            "print('Model loaded successfully for Grad-CAM inspection')"
        ]
    }
]

create_notebook(nb1_cells, "01_dataset_exploration.ipynb")
create_notebook(nb2_cells, "02_preprocessing.ipynb")
create_notebook(nb3_cells, "03_model_training.ipynb")
create_notebook(nb4_cells, "04_evaluation.ipynb")
create_notebook(nb5_cells, "05_gradcam.ipynb")
