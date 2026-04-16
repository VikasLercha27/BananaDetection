# Banana Detection

A mobile + backend project for banana detection and ripeness classification using deep learning.

The repo contains:

- `banana_detection_backend/` — FastAPI backend using EfficientNetB0 features and an ANN classifier.
- `banana_detection_frontend/` — Expo React Native app for capturing image input and sending predictions to the backend.

## Repository Structure

```text
Banana Project/
├── banana_detection_backend/
│   ├── api/app.py
│   ├── features_classifier/efficientnet/
│   ├── requirements.txt
│   └── README.md
├── banana_detection_frontend/
│   ├── App.js
│   ├── package.json
│   ├── src/
│   └── README.md
└── README.md
```

## Overview

This project enables users to capture or upload banana images from a mobile app and receive predictions from a backend service. The backend performs image feature extraction with EfficientNetB0 and uses a trained ANN model to classify the result.

## Quick Start

### Backend

1. Open a terminal in `banana_detection_backend/`
2. Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the backend:

```bash
python api/app.py
```

The API will be available at `http://localhost:8000`.

### Frontend

1. Open a terminal in `banana_detection_frontend/`
2. Install dependencies:

```bash
npm install
```

3. Start the Expo app:

```bash
npm start
```

4. Run on a device or emulator:

```bash
npm run android
npm run ios
npm run web
```

## Notes

- The frontend expects the backend on port `8000`.
- If using a physical device, make sure the device and development machine are on the same network.
- Backend predictions are sent to `POST /predict` as multipart form data.

## Full Documentation

For detailed configuration and usage, see:

- `banana_detection_backend/README.md`
- `banana_detection_frontend/README.md`

## License

This repository is part of the Banana Detection project.
