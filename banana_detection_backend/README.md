# Banana Detection Backend

## Overview

This backend serves the banana ripeness and artificial/natural banana detection API using a FastAPI service. The model uses EfficientNetB0 features plus a small ANN classifier to predict banana labels from uploaded images.

## Features

* REST API powered by FastAPI
* EfficientNetB0 feature extraction
* ANN classifier inference with saved scaler and label mapping
* Cross-origin requests enabled for mobile and web clients
* Health check endpoint and image prediction endpoint

## Requirements

* Python 3.10 or newer
* `fastapi`
* `uvicorn[standard]`
* `tensorflow>=2.15.0`
* `opencv-python-headless`
* `Pillow`
* `numpy`
* `scikit-learn`
* `joblib`

## Installation

1. Open a terminal in `banana_detection_backend`
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the backend server from the `banana_detection_backend` directory:

```bash
python api/app.py
```

The API will run at:

```text
http://localhost:8000
```

## API Endpoints

### GET /

Returns a simple status response with current model metadata.

### GET /health

Returns a health status: `{"status": "ok"}`.

### POST /predict

Accepts multipart form data with an image file and returns prediction details.

Request fields:

* `image` — image file upload
* `model` — optional model name, currently `ann_classifier`

Example request:

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "image=@banana.jpg" \
  -F "model=ann_classifier"
```

Example response:

```json
{
  "model": "ann_classifier",
  "backbone": "efficientnet",
  "prediction": 1,
  "label": "ripe",
  "confidence": 0.9876,
  "raw_prob": 0.9876
}
```

## Project Structure

```text
banana_detection_backend/
├── api/
│   └── app.py                   # FastAPI server
├── dataset/                     # image dataset folders
├── dataset_unseen/              # unseen evaluation datasets
├── features_classifier/         # saved model artifacts
│   └── efficientnet/
│       ├── ann_classifier.keras
│       ├── classes.npy
│       └── scaler.pkl
├── features_model/              # feature dataset files
├── graphs/                      # training / evaluation graphs
├── models/                      # trained model outputs
├── training/                    # training scripts
│   ├── explainmodel.py
│   ├── train_ann.py
│   ├── train_hparam_ann.py
│   ├── train_logistic.py
│   └── train_svc.py
├── requirements.txt
└── README.md
```

## Notes

* The FastAPI backend currently uses `features_classifier/efficientnet` as the model source.
* If you change the model or backbone, update `api/app.py` accordingly.
* Ensure the backend is running on port `8000` before connecting the frontend.

## License

This project is licensed under the MIT License.
