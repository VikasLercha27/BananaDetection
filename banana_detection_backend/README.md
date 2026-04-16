# Banana & Mango Ripeness Detection using Deep Learning

## Project Overview

This project implements a computer vision system for detecting the ripeness of bananas and mangoes using deep learning and machine learning techniques.

The system extracts visual features from fruit images using pretrained convolutional neural networks and trains multiple classifiers to determine the ripeness category. Multiple model–classifier combinations are evaluated to identify the best-performing solution.

The final system can be deployed through a REST API for real-time predictions.

---

# Problem Statement

Determining fruit ripeness is important in agriculture, food supply chains, and retail quality control. Manual inspection is subjective and inefficient.

This project provides an automated solution using computer vision and machine learning to classify fruit ripeness from images accurately and consistently.

---

# System Workflow

1. Image input and preprocessing
2. Feature extraction using pretrained CNN models
3. Feature scaling and transformation
4. Classification using machine learning models
5. Prediction served through a REST API

---

# Model Experimentation Strategy

This project evaluates multiple feature extraction models and classifiers to determine the most effective combination for ripeness detection.

## Feature Extraction Models

The following pretrained deep learning models are used to extract image features:

* MobileNetV2
* VGG16
* EfficientNet
* ConvNeXt

These networks generate high-level feature representations from fruit images.

## Classifiers Used

The extracted features are used to train different classifiers:

* Support Vector Machine (SVM)
* Logistic Regression
* Artificial Neural Network (ANN)

---

# Experimentation Pipeline

1. Preprocess fruit images (resize, normalize, clean dataset)
2. Extract deep features using CNN models
3. Train classifiers using extracted features
4. Evaluate model performance
5. Compare different model–classifier combinations
6. Select the best-performing model for final deployment

---

# Technologies Used

## Programming Language

* Python

## Deep Learning

* TensorFlow
* Keras

## Machine Learning

* Scikit-learn

## Computer Vision

* OpenCV
* PIL

## Backend / API

* Flask

## Data Processing

* NumPy

---

# Project Structure

```
banana-mango-ripeness-detection/

api/
  app.py                 → REST API for predictions

training/
  train_ann.py           → ANN training
  train_cnn.py           → CNN utilities
  train_logistic.py      → Logistic regression training
  train_svc.py           → SVM training

efficientnet/
  train_efficientnet.py  → EfficientNet training

features/
  extract_features_vgg16.py
  feature_extractor_mobilenet.py
  convnext.py

models/
  → stored trained models and scalers

service.py
service_vgg16.py
utils.py
requirements.txt
README.md
```

---

# Installation

Clone the repository:

```
git clone https://github.com/VikasLercha27/BananaDetection
cd BananaDetection
```

Create a virtual environment:

```
python -m venv venv
```

Activate environment

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Training Models

Train different classifiers using the provided scripts:

```
python training/train_svc.py
python training/train_ann.py
python efficientnet/train_efficientnet.py
```

---

# Running the API

Start the Flask API server:

```
python api/app.py
```

API will run at:

```
http://localhost:5000
```

---

# Example API Request

```
curl -X POST -F "image=@banana.jpg" \
     -F "backbone=mobilenet" \
     -F "classifier=svc" \
     http://localhost:5000/predict
```

### Example Response

```
{
  "prediction": "ripe",
  "confidence": 0.92,
  "backbone": "mobilenet",
  "classifier": "svc"
}
```

---

# Future Improvements

* Model optimization for edge deployment
* Real-time fruit detection from video streams
* Support for additional fruit categories
* Web interface for easy interaction
* Ensemble learning for improved accuracy
* Data augmentation for better model robustness
* Frontend web or mobile interface for uploading fruit images and viewing ripeness predictions.
---

# Author

Vikas Lercha
B.Tech – Computer Science Engineering

---

# License

This project is licensed under the MIT License.
