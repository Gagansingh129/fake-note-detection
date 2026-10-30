# NoteGuard AI - Complete Windows Setup Guide

This guide walks you through setting up **NoteGuard AI** on Windows with Python 3.11 and Node.js.

---

## 1. Environment Verification

Confirm that your tools are available in PowerShell:
```powershell
py -3.11 --version
node --version
npm --version
```

If `py -3.11` is present, you are ready to proceed.

---

## 2. Virtual Environment Setup

From the project root directory (`Fake Note Detection`):

```powershell
# Create a dedicated virtual environment with Python 3.11
py -3.11 -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

> **Note on PowerShell Execution Policy:** If you encounter a script execution error when running `Activate.ps1`, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## 3. Directory Layout & Placing Your Dataset

Place your curated research images into `dataset/raw/`. The dataset preparation script supports two flexible directory structures:

### Structure A: By Denomination (Recommended)
```
dataset/raw/
├── 100/
│   ├── genuine/   (image1.jpg, image2.jpg...)
│   └── fake/      (image3.jpg, image4.jpg...)
├── 500/
│   ├── genuine/
│   └── fake/
```

### Structure B: Binary Only
```
dataset/raw/
├── genuine/   (real note images)
└── fake/      (counterfeit screening sample images)
```

Run dataset preparation (Phase 2):
```powershell
python training/prepare_dataset.py
```

---

## 4. Running the FastAPI Backend

```powershell
# From the project root with venv activated:
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/health`

---

## 5. Running the React + Vite Frontend

In a second terminal window:
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 6. Testing the Camera
1. Navigate to the **Analyze** page.
2. Select **Use Camera**.
3. Allow the browser camera permission when prompted.
4. Align the note inside the on-screen rectangular framing guide.
5. Click **Capture** and then **Analyze Note**.
