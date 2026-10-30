# NoteGuard AI: Indian Currency Note Authenticity Detection System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-cyan.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.x-purple.svg)](https://vitejs.dev/)

> **Academic Disclaimer:** NoteGuard AI is an academic computer-vision screening research project. It does **not** claim to provide legally definitive authentication of currency. Predictions are AI-based screening approximations influenced by image resolution, lighting conditions, camera angles, perspective distortion, and training dataset representation. High-stakes currency verification must always adhere to authorized banking and forensic verification procedures.

---

## 1. Problem Statement
Circulation of counterfeit Indian banknotes poses economic challenges and risks to financial institutions, retail vendors, and ordinary citizens. Traditional verification relies either on expensive specialized hardware or manual inspection of tactile and optical security features (e.g., security thread, watermark, latent image, bleed lines). A fast, accessible, software-assisted screening tool that works via consumer cameras or uploaded photographs can serve as a first-line pre-screening mechanism.

## 2. Project Objectives
- Develop an end-to-end deep learning pipeline for Indian currency denomination identification and counterfeit screening.
- Support denominations: ₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹2000.
- Provide explainable AI diagnostics via **Grad-CAM** (Gradient-weighted Class Activation Mapping) to highlight visual regions guiding model decisions.
- Implement an automated image quality assessment layer (blur estimation via Laplacian variance, brightness analysis, resolution verification).
- Deliver a production-grade full-stack web application featuring:
  - Responsive web dashboard (React + Vite).
  - Real-time webcam/mobile camera stream with bounding alignment guides.
  - Asynchronous RESTful backend (FastAPI + SQLAlchemy + SQLite).
  - Prediction audit history with exportable records.

---

## 3. High-Level Architecture

```
[ User Device / Browser ]
        │
        ├─► Mode 1: Static Image Upload (JPG/PNG/WEBP)
        └─► Mode 2: Live Camera Capture (MediaDevices WebRTC API)
                    │
                    ▼
          [ React + Vite UI ]
                    │ HTTP multipart/form-data
                    ▼
         [ FastAPI Application ]
                    │
                    ├─► 1. File Type & Size Validation
                    ├─► 2. Image Quality Assessment (Blur / Brightness / Resolution)
                    ├─► 3. Preprocessing (224x224 RGB, Color Normalization)
                    ├─► 4. Deep Learning Inference:
                    │      ├── Stage 1: Denomination Classifier (₹10 - ₹2000)
                    │      └── Stage 2: Authenticity Classifier (Genuine vs Counterfeit)
                    ├─► 5. Grad-CAM Visual Heatmap Generation
                    ├─► 6. Persistence: SQLite Audit Table
                    │
                    ▼
          [ JSON Prediction Response ]
          - Denomination
          - Authenticity Label
          - Confidence Score
          - Quality Metrics
          - Grad-CAM Heatmap URL
```

---

## 4. Technology Stack

| Domain | Technologies |
|---|---|
| **Deep Learning & CV** | Python 3.11, TensorFlow / Keras, OpenCV, NumPy, Scikit-learn, PIL |
| **Explainable AI (XAI)** | Grad-CAM (Target Convolutional Activation Maps) |
| **Backend & API** | FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic v2 |
| **Frontend UI** | React 18, Vite, Lucide Icons, Modern CSS3 |
| **Evaluation & Plotting** | Matplotlib, Seaborn, Pandas |

---

## 5. Dataset Organization

NoteGuard AI supports hierarchical multi-denomination datasets as well as flat binary classification structures.

```
dataset/
├── raw/                      # Original uncurated images
├── processed/                # Cleaned, standardized 224x224 images
├── train/
│   ├── 100/
│   │   ├── genuine/
│   │   └── fake/
│   ├── 200/
│   │   ├── genuine/
│   │   └── fake/
│   └── 500/
│       ├── genuine/
│       └── fake/
├── validation/               # 15% split
└── test/                     # 15% split (unseen holdout)
```

*(Alternatively, flat binary structure `train/genuine` and `train/fake` is dynamically supported).*

---

## 6. Directory Structure

```
NoteGuard-AI/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entrypoint
│   │   ├── config.py                  # App configuration & thresholds
│   │   ├── database.py                # SQLAlchemy SQLite session engine
│   │   ├── models.py                  # Database entities
│   │   ├── schemas.py                 # Pydantic request/response schemas
│   │   ├── routes/
│   │   │   ├── prediction.py          # Prediction endpoint
│   │   │   ├── camera.py              # Camera stream upload endpoint
│   │   │   └── history.py             # History query & deletion
│   │   ├── services/
│   │   │   ├── preprocessing.py       # Image normalization & quality checks
│   │   │   ├── prediction_service.py  # Inference orchestration
│   │   │   ├── gradcam.py             # Gradient class activation mapping
│   │   │   └── image_processing.py    # Computer vision filters & checks
│   │   └── utils/
│   │       └── helpers.py             # File utils & validators
│   ├── models/                        # Stored .keras models & label maps
│   ├── uploads/                       # Ephemeral upload storage
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/                # CameraCapture, ImageUpload, GradCAMViewer, etc.
│   │   ├── pages/                     # Home, Analyze, History, About
│   │   ├── services/api.js            # Axios/Fetch API client
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── dataset/                           # Raw & split datasets
├── notebooks/                         # 5 step-by-step Jupyter notebooks
├── training/                          # Dataset prep, baseline, and transfer training scripts
├── results/                           # Evaluation graphs, confusion matrices, and Grad-CAM logs
├── README.md
├── SETUP_GUIDE.md
└── requirements.txt
```

---

## 7. Quick Start (Windows)

### Prerequisites
- Python 3.11 (`py -3.11`)
- Node.js (v18+) & npm

### Backend Setup
```powershell
# In project root:
py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Start Backend Server
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```powershell
# In a separate terminal:
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the NoteGuard AI web application.

---

## 8. Limitations & Ethical Considerations
- **No Counterfeit Generation:** This project does not generate synthetic counterfeit bills or provide instructions for illicit duplication.
- **Environmental Factors:** Model predictions are susceptible to poor ambient illumination, camera shake, severe creasing, or partial occlusion.
- **Screening Only:** Always verify currency through official banking channels.
