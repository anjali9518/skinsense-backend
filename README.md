# SkinGuardian - AI Skin Cancer Detection

A full-stack application that uses a trained deep learning model to classify skin lesions into 8 categories. It consists of a Flask REST API backend and a React (Vite + TypeScript) frontend.

## Project Structure

```
mysite/
├── api.py                              # Flask API server (run this)
├── app.py                              # Legacy Flask app (HTML templates, not used by React UI)
├── config.py                           # Flask config
├── requirements.txt                    # Python dependencies
├── SkinCancerClassificationModelhdf5nc.h5  # Trained model (not in repo — see below)
├── static/uploads/                     # Uploaded images (created automatically)
├── templates/                          # Legacy HTML templates
└── ui_design_project/skin-guardian/    # React frontend
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm 9+

## Setup

### 1. Backend (Flask API)

```bash
# Navigate to project root
cd mysite

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download the Model

The trained model file `SkinCancerClassificationModelhdf5nc.h5` is not included in the repo due to its size (15 MB). Place it in the project root (`mysite/`) before starting the backend.

### 3. Frontend (React)

```bash
cd ui_design_project/skin-guardian
npm install
```

## Running the Application

### Start the Backend

```bash
# From project root, with venv activated
python api.py
```

The API server starts on `http://localhost:2500`. You should see:
```
Loading ML model...
Model loaded successfully
API Server starting on http://0.0.0.0:2500
```

### Start the Frontend

```bash
# In a separate terminal
cd ui_design_project/skin-guardian
npm run dev
```

The frontend starts on `http://localhost:8080`.

### Use the App

1. Open `http://localhost:8080` in your browser
2. Go to **SkinSense** to upload a skin lesion image and get an AI diagnosis
3. Go to **Learn** to read about skin cancer types, detection methods, and prevention

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check — confirms server and model status |
| POST | `/api/analyze` | Upload an image for classification (multipart form, field: `file`) |
| GET | `/api/info` | Returns all 8 classification types with descriptions |
| GET | `/api/images/<filename>` | Serves an uploaded image |

## Cancer Classifications

The model detects 8 categories:

| # | Classification | Severity |
|---|----------------|----------|
| 0 | Actinic keratoses | Moderate |
| 1 | Basal Cell Carcinoma | High |
| 2 | Benign Keratosis | Low |
| 3 | Dermatofibroma | Low |
| 4 | Melanocytic nevus | Low |
| 5 | Vascular Lesion | Low |
| 6 | Melanoma | Critical |
| 7 | No Cancer Detected | None |

## Tech Stack

**Backend:** Flask, TensorFlow/Keras, NumPy, Pillow
**Frontend:** React, TypeScript, Vite, Tailwind CSS, Framer Motion, shadcn/ui

## Disclaimer

This tool is for **educational purposes only** and is not a substitute for professional medical advice. Always consult a dermatologist for skin concerns.
