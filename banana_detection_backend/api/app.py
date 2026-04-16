# import os
# import sys
# import numpy as np
# import cv2
# import joblib
# import tensorflow as tf
# from flask import Flask, request, jsonify
# from PIL import Image
# from flask_cors import CORS
# from io import BytesIO

# # ---------------------------
# # Setup paths
# # ---------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

# from service import extract_features_from_array as mobilenet_features
# # from service_vgg16 import extract_features_from_array as vgg16_features


# # ---------------------------
# # Flask app
# # ---------------------------
# app = Flask(__name__)
# CORS(app)


# # ---------------------------
# # LOAD MODELS ONCE
# # ---------------------------
# models = {}

# for backbone in ["mobilenet"]:

#     MODEL_DIR = os.path.join(BASE_DIR, "models", backbone)

#     models[backbone] = {
#         "logistic": joblib.load(os.path.join(MODEL_DIR, "logistic_classifier.pkl")),
#         "svc": joblib.load(os.path.join(MODEL_DIR, "svm_classifier.pkl")),
#         "ann": tf.keras.models.load_model(os.path.join(MODEL_DIR, "ann_classifier.h5")),
#         "scaler": joblib.load(os.path.join(MODEL_DIR, "feature_scaler.pkl")),
#         "classes": np.load(os.path.join(MODEL_DIR, "classes.npy"))
#     }

# print("Models loaded successfully")


# # ---------------------------
# # Image loader
# # ---------------------------
# def load_image(file):

#     file.seek(0)
#     image_bytes = file.read()

#     if not image_bytes:
#         raise ValueError("Uploaded file is empty")

#     try:
#         file_array = np.frombuffer(image_bytes, np.uint8)
#         img = cv2.imdecode(file_array, cv2.IMREAD_COLOR)

#         if img is not None:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             img = cv2.resize(img, (224, 224))
#             return img
#     except:
#         pass

#     try:
#         img = Image.open(BytesIO(image_bytes)).convert("RGB")
#         img = img.resize((224, 224))
#         return np.array(img)

#     except Exception as e:
#         raise ValueError(f"Image decoding failed: {str(e)}")


# # ---------------------------
# # Prediction route
# # ---------------------------
# @app.route("/predict", methods=["POST"])
# def predict():

#     print("FILES:", request.files)
#     print("FORM:", request.form)

#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image = request.files["image"]

#     model_name = request.form.get("model", "ann_classifier")
#     backbone = request.form.get("backbone", "mobilenet")

#     try:

#         model_pack = models.get(backbone)

#         if model_pack is None:
#             return jsonify({"error": "Invalid backbone"}), 400

#         logistic_model = model_pack["logistic"]
#         svc_model = model_pack["svc"]
#         ann_model = model_pack["ann"]
#         scaler = model_pack["scaler"]
#         classes = model_pack["classes"]

#         img_array = load_image(image)

#         # ---------------------------
#         # Feature extraction
#         # ---------------------------
#         if backbone == "mobilenet":
#             features = mobilenet_features(img_array)

#         elif backbone == "vgg16":
#             features = vgg16_features(img_array)

#         else:
#             return jsonify({"error": "Invalid backbone"}), 400

#         features = scaler.transform(features)

#         # ---------------------------
#         # Prediction
#         # ---------------------------
#         if model_name == "logistic":

#             prediction = logistic_model.predict(features)[0]
#             confidence = logistic_model.predict_proba(features)[0][1]

#         elif model_name == "svc":

#             prediction = svc_model.predict(features)[0]
#             confidence = svc_model.predict_proba(features)[0][1]

#         elif model_name == "ann_classifier":

#             prob = ann_model.predict(features)[0][0]
#             prediction = int(prob > 0.5)
#             confidence = float(prob)

#         else:
#             return jsonify({"error": "Invalid model name"}), 400

#         label = classes[int(prediction)]

#         return jsonify({
#             "model": model_name,
#             "backbone": backbone,
#             "prediction": int(prediction),
#             "label": str(label),
#             "confidence": float(confidence)
#         })

#     except Exception as e:

#         print("SERVER ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500


# # ---------------------------
# # Run server
# # ---------------------------
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)  
# ============================================================
# main.py — FastAPI backend for Ripen AI
# EfficientNetB0 + ANN classifier
# ============================================================
# ============================================================
# main.py — FastAPI backend for Ripen AI
# EfficientNetB0 + ANN classifier
# ============================================================
# ============================================================
# main.py — FastAPI backend for Ripen AI
# EfficientNetB0 + ANN classifier
# ============================================================

# import os
# import sys
# import numpy as np
# import cv2
# import joblib
# from io import BytesIO
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from PIL import Image
# import tensorflow as tf
# from tensorflow.keras.applications import EfficientNetB0
# from tensorflow.keras.applications.efficientnet import preprocess_input

# # ── Paths ───────────────────────────────────────────────────────
# # main.py lives in:  d:\mango_detection\api\
# # models live in:    d:\mango_detection\models\efficientnet\
# BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "models", "efficientnet")

# # ── EfficientNetB0 backbone (loaded once at startup) ────────────
# backbone = EfficientNetB0(
#     weights="imagenet",
#     include_top=False,
#     input_shape=(224, 224, 3),
#     pooling="avg"
# )

# # ── ANN model + scaler + classes ────────────────────────────────
# ann_model = tf.keras.models.load_model(
#     os.path.join(MODEL_DIR, "ann_classifier.keras")
# )
# scaler  = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
# classes = np.load(os.path.join(MODEL_DIR, "classes.npy"), allow_pickle=True).tolist()

# print("✅ All models loaded successfully")
# print(f"   Classes : {classes}")
# print(f"   Feature dim will be: 1287 (1280 CNN + 7 colour)")


# # ── Feature extraction ───────────────────────────────────────────
# def extract_color_features(img_rgb: np.ndarray) -> np.ndarray:
#     """
#     Extracts 7 colour features — MUST match extract_features.py exactly:
#     [mean_H, std_H, mean_S, std_S, mean_V, mean_A, mean_B]
#     """
#     hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
#     h, s, v = cv2.split(hsv)

#     lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
#     l, a, b = cv2.split(lab)

#     return np.array([
#         np.mean(h), np.std(h),
#         np.mean(s), np.std(s),
#         np.mean(v),
#         np.mean(a), np.mean(b)
#     ])


# def extract_features(img_rgb: np.ndarray) -> np.ndarray:
#     """
#     Full pipeline:
#       RGB image (224×224) → EfficientNet (1280) + colour (7) → (1, 1287)
#     """
#     img_input  = np.expand_dims(img_rgb, axis=0)
#     img_input  = preprocess_input(img_input.astype(np.float32))
#     cnn_feat   = backbone.predict(img_input, verbose=0).squeeze()   # (1280,)
#     color_feat = extract_color_features(img_rgb)                    # (7,)
#     features   = np.concatenate([cnn_feat, color_feat])            # (1287,)
#     return features.reshape(1, -1)                                  # (1, 1287)


# # ── Image loader ─────────────────────────────────────────────────
# def load_image(file_bytes: bytes) -> np.ndarray:
#     """
#     Loads image bytes → RGB numpy array (224×224×3).
#     Tries OpenCV first, falls back to PIL.
#     """
#     try:
#         arr = np.frombuffer(file_bytes, np.uint8)
#         img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
#         if img is not None:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             img = cv2.resize(img, (224, 224))
#             return img
#     except Exception:
#         pass

#     try:
#         img = Image.open(BytesIO(file_bytes)).convert("RGB")
#         img = img.resize((224, 224))
#         return np.array(img)
#     except Exception as e:
#         raise ValueError(f"Image decoding failed: {e}")


# # ── FastAPI app ──────────────────────────────────────────────────
# app = FastAPI(
#     title="Ripen AI — Mango Detection API",
#     description="EfficientNetB0 + ANN classifier for natural vs artificial mango detection",
#     version="2.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ── Health check ─────────────────────────────────────────────────
# @app.get("/")
# async def root():
#     return {
#         "status"  : "running",
#         "model"   : "EfficientNetB0 + ANN",
#         "classes" : classes,
#         "version" : "2.0.0"
#     }

# @app.get("/health")
# async def health():
#     return {"status": "ok"}


# # ── Prediction endpoint ──────────────────────────────────────────
# @app.post("/predict")
# async def predict(
#     image: UploadFile = File(...),
#     model: str        = Form(default="ann_classifier"),
# ):
#     # ── Validate file type ──────────────────────────────────────
#     if not image.content_type.startswith("image/"):
#         raise HTTPException(
#             status_code=400,
#             detail=f"File must be an image. Got: {image.content_type}"
#         )

#     try:
#         # ── Read & decode image ─────────────────────────────────
#         file_bytes = await image.read()
#         if not file_bytes:
#             raise HTTPException(status_code=400, detail="Uploaded file is empty")

#         img_array = load_image(file_bytes)

#         # ── Extract features ────────────────────────────────────
#         features        = extract_features(img_array)       # (1, 1287)
#         features_scaled = scaler.transform(features)        # (1, 1287) scaled

#         # ── Run ANN prediction ──────────────────────────────────
#         if model == "ann_classifier":
#             prob       = float(ann_model.predict(features_scaled, verbose=0)[0][0])
#             prediction = int(prob >= 0.5)
#             confidence = prob

#         else:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Unknown model: '{model}'. Available: ann_classifier"
#             )

#         label = classes[prediction]

#         # Confidence from the perspective of the predicted class
#         display_confidence = confidence if prediction == 1 else 1.0 - confidence

#         return JSONResponse({
#             "model"      : model,
#             "backbone"   : "efficientnet",
#             "prediction" : prediction,
#             "label"      : str(label),
#             "confidence" : round(display_confidence, 4),
#             "raw_prob"   : round(prob, 4),
#         })

#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"[ERROR] /predict → {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # ── Run ──────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
# ============================================================
# app.py — FastAPI backend for Banana Detection API
# EfficientNetB0 + ANN classifier
# ============================================================

import os
import sys
import numpy as np
import cv2
import joblib
from io import BytesIO

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

# ── Paths ────────────────────────────────────────────────────────
# app.py lives in:  d:\banana_detection_backend\api\
# models live in:   d:\banana_detection_backend\features_classifier\efficientnet\
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "features_classifier", "efficientnet")

# ── EfficientNetB0 backbone (loaded once at startup) ─────────────
backbone = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3),
    pooling="avg"
)

# ── ANN model + scaler + classes ─────────────────────────────────
ann_model = tf.keras.models.load_model(
    os.path.join(MODEL_DIR, "ann_classifier.keras")
)
scaler  = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
classes = np.load(
    os.path.join(MODEL_DIR, "classes.npy"), allow_pickle=True
).tolist()

print("✅ All models loaded successfully")
print(f"   MODEL_DIR : {MODEL_DIR}")
print(f"   Classes   : {classes}")
print(f"   Feature dim: 1287 (1280 CNN + 7 colour)")


# ── Feature extraction ────────────────────────────────────────────
def extract_color_features(img_rgb: np.ndarray) -> np.ndarray:
    """
    7 colour features — must match feature_extractor_efficientnet.py exactly:
    [mean_H, std_H, mean_S, std_S, mean_V, mean_A, mean_B]
    """
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    return np.array([
        np.mean(h), np.std(h),
        np.mean(s), np.std(s),
        np.mean(v),
        np.mean(a), np.mean(b)
    ])


def extract_features(img_rgb: np.ndarray) -> np.ndarray:
    """
    RGB image (224×224) → EfficientNet (1280) + colour (7) → (1, 1287)
    """
    img_input  = np.expand_dims(img_rgb, axis=0)
    img_input  = preprocess_input(img_input.astype(np.float32))
    cnn_feat   = backbone.predict(img_input, verbose=0).squeeze()  # (1280,)
    color_feat = extract_color_features(img_rgb)                   # (7,)
    features   = np.concatenate([cnn_feat, color_feat])           # (1287,)
    return features.reshape(1, -1)                                 # (1, 1287)


# ── Image loader ──────────────────────────────────────────────────
def load_image(file_bytes: bytes) -> np.ndarray:
    """
    Loads image bytes → RGB numpy array (224×224×3).
    Tries OpenCV first, falls back to PIL.
    """
    try:
        arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            return img
    except Exception:
        pass

    try:
        img = Image.open(BytesIO(file_bytes)).convert("RGB")
        img = img.resize((224, 224))
        return np.array(img)
    except Exception as e:
        raise ValueError(f"Image decoding failed: {e}")


# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(
    title="Banana Detection API",
    description="EfficientNetB0 + ANN classifier for natural vs artificial banana detection",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health check ──────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "status"  : "running",
        "model"   : "EfficientNetB0 + ANN",
        "classes" : classes,
        "version" : "2.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Prediction endpoint ───────────────────────────────────────────
@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    model: str        = Form(default="ann_classifier"),
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"File must be an image. Got: {image.content_type}"
        )

    try:
        file_bytes = await image.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        img_array = load_image(file_bytes)

        # Features are already scaled by the extractor,
        # but we apply the saved scaler here for inference consistency
        features        = extract_features(img_array)       # (1, 1287) raw
        features_scaled = scaler.transform(features)        # (1, 1287) scaled

        if model == "ann_classifier":
            prob       = float(ann_model.predict(features_scaled, verbose=0)[0][0])
            prediction = int(prob >= 0.5)
            confidence = prob
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown model: '{model}'. Available: ann_classifier"
            )

        label = classes[prediction]
        display_confidence = confidence if prediction == 1 else 1.0 - confidence

        return JSONResponse({
            "model"      : model,
            "backbone"   : "efficientnet",
            "prediction" : prediction,
            "label"      : str(label),
            "confidence" : round(display_confidence, 4),
            "raw_prob"   : round(prob, 4),
        })

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] /predict → {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Run ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)