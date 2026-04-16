# print("Training ANN classifier")
# BACKBONE = "vgg16"   # change to "vgg16" when needed

# import numpy as np
# import joblib
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout
# from tensorflow.keras.callbacks import EarlyStopping
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report
# import psutil
# import os
# from tensorflow.keras.layers import BatchNormalization, Input
# from tensorflow.keras.regularizers import l2
# from tensorflow.keras.regularizers import l1
# FEATURE_DIR = f"features/{BACKBONE}"
# MODEL_DIR = f"models/{BACKBONE}"
# os.makedirs(MODEL_DIR, exist_ok=True)
# # ----------------------------
# # MEMORY FUNCTION
# # ----------------------------
# def print_memory(stage):
#     process = psutil.Process(os.getpid())
#     memory = process.memory_info().rss / (1024 * 1024)  # MB
#     print(f"[{stage}] RAM Usage: {memory:.2f} MB")


# print_memory("Start")

# # ----------------------------
# # LOAD FEATURES
# # ----------------------------
# X_train = np.load(f"{FEATURE_DIR}/X_train.npy")
# y_train = np.load(f"{FEATURE_DIR}/y_train.npy")

# X_val = np.load(f"{FEATURE_DIR}/X_val.npy")
# y_val = np.load(f"{FEATURE_DIR}/y_val.npy")

# X_test = np.load(f"{FEATURE_DIR}/X_test.npy")
# y_test = np.load(f"{FEATURE_DIR}/y_test.npy")

# print("Features loaded")
# print_memory("After Loading Data")


# # ----------------------------
# # SCALE DATA
# # ----------------------------
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_val = scaler.transform(X_val)
# X_test = scaler.transform(X_test)

# print_memory("After Scaling")


# # ----------------------------
# # BUILD ANN MODEL
# # ----------------------------


# model = Sequential([
#     Input(shape=(X_train.shape[1],)),

#     Dense(1024, kernel_regularizer=l2(0.001)),
#     BatchNormalization(),
#     tf.keras.layers.Activation('relu'),
#     Dropout(0.1),

#     Dense(512, kernel_regularizer=l2(0.001)),
#     BatchNormalization(),
#     tf.keras.layers.Activation('relu'),
#     Dropout(0.1),

#     Dense(1, activation='sigmoid')
# ])



# model.compile(
#     optimizer='adam',
#     loss='binary_crossentropy',
#     metrics=['accuracy']
# )
# print("Learning Rate:", model.optimizer.learning_rate.numpy())

# model.summary()
# print_memory("After Model Build")


# # ----------------------------
# # TRAIN MODEL
# # ----------------------------
# early_stop = EarlyStopping(
#     monitor='val_loss',
#     patience=20,
#     restore_best_weights=True
# )

# print_memory("Before Training")

# history = model.fit(
#     X_train, y_train,
#     validation_data=(X_val, y_val),
#     epochs=50,
#     batch_size=32,
#     callbacks=[early_stop],
#     verbose=1
# )

# print_memory("After Training")

# # ----------------------------
# # EVALUATION
# # ----------------------------
# train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
# val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
# test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

# print("Train Accuracy:", train_acc)
# print("Val Accuracy:", val_acc)
# print("Test Accuracy:", test_acc)

# print_memory("After Evaluation")

# y_pred = (model.predict(X_test) > 0.5).astype("int32")
# print_memory("After Prediction")

# print("\nTest Classification Report:")
# print(classification_report(y_test, y_pred))

# # ----------------------------
# # SAVE MODEL
# # ----------------------------
# model.save(f"{MODEL_DIR}/ann_classifier.h5")
# joblib.dump(scaler, f"{MODEL_DIR}/feature_scaler.pkl")

# print("Model and scaler saved")

# print_memory("After Saving Model")

# # ----------------------------
# # MODEL SIZE ON DISK
# # ----------------------------
# size = os.path.getsize(f"{MODEL_DIR}/ann_classifier.h5") / (1024 * 1024)
# print(f"ANN model size: {size:.2f} MB")

# print("Training ANN classifier")

# BACKBONE = "efficientnet"   # change to "vgg16" when needed

# import os
# import numpy as np
# import joblib
# import psutil
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import (
#     Dense, Dropout, BatchNormalization,
#     Activation, Input
# )
# from tensorflow.keras.regularizers import l2
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
# from tensorflow.keras.metrics import Precision, Recall, AUC
# from sklearn.metrics import classification_report

# FEATURE_DIR = f"features/{BACKBONE}"
# MODEL_DIR   = f"models/{BACKBONE}"
# os.makedirs(MODEL_DIR, exist_ok=True)


# # ── Helpers ───────────────────────────────────────────────────
# def print_memory(stage: str) -> None:
#     mb = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)
#     print(f"  [RAM | {stage}] {mb:.1f} MB")


# # ── 1. Load pre-extracted features ───────────────────────────
# print("\n[1/5] Loading features …")
# print_memory("start")

# X_train = np.load(f"{FEATURE_DIR}/X_train.npy")
# y_train = np.load(f"{FEATURE_DIR}/y_train.npy")
# X_val   = np.load(f"{FEATURE_DIR}/X_val.npy")
# y_val   = np.load(f"{FEATURE_DIR}/y_val.npy")
# X_test  = np.load(f"{FEATURE_DIR}/X_test.npy")
# y_test  = np.load(f"{FEATURE_DIR}/y_test.npy")

# print(f"  Train : {X_train.shape}  Val : {X_val.shape}  Test : {X_test.shape}")
# print_memory("after load")


# # ── 2. Load the scaler saved during feature extraction ────────
# # FIX: do NOT refit a new scaler here — reuse the one already
# #      fitted on train during extract_features.py so inference
# #      time scaling is consistent.
# print("\n[2/5] Loading saved scaler …")
# scaler_path = f"{MODEL_DIR}/scaler.pkl"

# if os.path.exists(scaler_path):
#     scaler = joblib.load(scaler_path)
#     print("  Loaded existing scaler from disk.")
# else:
#     # Fallback: fit here and warn — ideally should come from extraction
#     from sklearn.preprocessing import StandardScaler
#     print("  WARNING: no saved scaler found — fitting a new one.")
#     print("  Re-run extract_features.py to generate a consistent scaler.")
#     scaler = StandardScaler()
#     scaler.fit(X_train)
#     joblib.dump(scaler, scaler_path)

# X_train = scaler.transform(X_train)
# X_val   = scaler.transform(X_val)
# X_test  = scaler.transform(X_test)
# print_memory("after scaling")


# print("\n[3/5] Building model …")

# input_dim = X_train.shape[1]   # 1335 for EfficientNetB0 + colour

# model = Sequential([
#     Input(shape=(input_dim,)),

#     # Block 1
#     Dense(64, kernel_regularizer=l1(0.001)),
#     BatchNormalization(),
#     Activation('sigmoid'),  # smoother than ReLU, helps with train/val gap
#     Dropout(0.4),               # was 0.1 — primary fix for train/val gap

#     # Block 2
#     Dense(128, kernel_regularizer=l1(0.001)),
#     BatchNormalization(),
#     Activation('sigmoid'),  # smoother than ReLU, helps with train/val gap
#     Dropout(0.3),               # gradually lower dropout toward output

#     # Output
#     Dense(1, activation='sigmoid')
# ], name="mango_ann")

# model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
#     loss='binary_crossentropy',
#     metrics=[
#         'accuracy',
#         Precision(name='precision'),
#         Recall(name='recall'),
#         AUC(name='auc_pr', curve='PR'),
#     ]
# )

# print(f"  Input dim : {input_dim}")
# print(f"  LR        : {model.optimizer.learning_rate.numpy():.4f}")
# model.summary()
# print_memory("after model build")


# # ── 4. Train ──────────────────────────────────────────────────
# print("\n[4/5] Training …")

# callbacks = [
#     # Stop when val_loss stops improving
#     EarlyStopping(
#         monitor='val_loss',
#         patience=10,            # was 20 — tighter, less overtraining
#         restore_best_weights=True,
#         verbose=1,
#     ),
#     # Halve LR when val_loss plateaus for 5 epochs
#     ReduceLROnPlateau(
#         monitor='val_loss',
#         factor=0.5,
#         patience=5,
#         min_lr=1e-6,
#         verbose=1,
#     ),
# ]

# print_memory("before training")

# history = model.fit(
#     X_train, y_train,
#     validation_data=(X_val, y_val),
#     epochs=100,                 # let early stopping decide when to quit
#     batch_size=64,              # was 32 — smoother gradients
#     callbacks=callbacks,
#     verbose=1,
# )

# print_memory("after training")


# # ── 5. Evaluate ───────────────────────────────────────────────
# print("\n[5/5] Evaluating …")

# def evaluate_split(name, X, y):
#     results = model.evaluate(X, y, verbose=0)
#     metric_names = [m.name for m in model.metrics]
#     print(f"\n  {name}")
#     for n, v in zip(metric_names, results):
#         print(f"    {n:12s}: {v:.4f}")

# evaluate_split("Train", X_train, y_train)
# evaluate_split("Val",   X_val,   y_val)
# evaluate_split("Test",  X_test,  y_test)

# print_memory("after evaluation")

# # Detailed test report
# y_pred = (model.predict(X_test, verbose=0) > 0.5).astype("int32")
# classes = np.load(f"{MODEL_DIR}/classes.npy", allow_pickle=True).tolist()

# print("\n  Test classification report:")
# print(classification_report(y_test, y_pred, target_names=classes))
# print_memory("after prediction")


# # ── Save ──────────────────────────────────────────────────────
# model_path = f"{MODEL_DIR}/ann_classifier.keras"   # .keras > .h5 in TF2
# model.save(model_path)
# print(f"\n  Model saved  → {model_path}")

# size_mb = os.path.getsize(model_path) / (1024 ** 2)
# print(f"  Model size   : {size_mb:.2f} MB")
# print_memory("after save")
# ============================================================
# train_ann.py — ANN classifier on EfficientNet + colour features
# Best configuration from Run 376 (hyperparameter_experiments_v2)
#   Neurons     : 64 → 128
#   Activation  : sigmoid
#   L1 & L2 Reg : 0.001
#   Learning Rate: 0.2
#   Dropout     : 0.5 (L1), 0.4 (L2)
#   Batch Size  : 50
#   Max Epochs  : 200 (early stopping active)
# Results       : Val=0.9802, Test=0.9837, F1=0.9836 (Rank #1)
# ============================================================

print("Training ANN classifier")

BACKBONE = "efficientnet"

import os
import numpy as np
import joblib
import psutil
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense, Dropout, BatchNormalization,
    Activation, Input
)
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.metrics import Precision, Recall, AUC
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report

# ── Directory paths (absolute, resolved relative to this script) ───
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURE_DIR = os.path.join(BASE_DIR, "features_model", BACKBONE)      # X_train/val/test .npy files live here
MODEL_DIR   = os.path.join(BASE_DIR, "features_classifier", BACKBONE)  # scaler.pkl lives here
CLASSES_DIR = os.path.join(BASE_DIR, "features_classifier", BACKBONE)  # classes.npy lives here
OUTPUT_DIR  = os.path.join(BASE_DIR, "features_classifier", BACKBONE)  # save model + scaler here

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Best hyperparameters from Run 376 ─────────────────────────
NEURONS_L1    = 64        # Dense Layer 1 neurons
NEURONS_L2    = 128       # Dense Layer 2 neurons
ACTIVATION    = 'sigmoid' # Run 376 uses sigmoid, not relu
L1_REG        = 0.001
L2_REG        = 0.001
LEARNING_RATE = 0.2       # Run 376 LR — ReduceLROnPlateau handles decay
DROPOUT_L1    = 0.5
DROPOUT_L2    = 0.4
BATCH_SIZE    = 50
MAX_EPOCHS    = 200
ES_PATIENCE   = 10
LR_PATIENCE   = 5


# ── Helpers ───────────────────────────────────────────────────
def print_memory(stage: str) -> None:
    mb = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)
    print(f"  [RAM | {stage}] {mb:.1f} MB")


# ── 1. Load pre-extracted features ───────────────────────────
print("\n[1/5] Loading features …")
print_memory("start")

X_train = np.load(os.path.join(FEATURE_DIR, "X_train.npy"))
y_train = np.load(os.path.join(FEATURE_DIR, "y_train.npy"))
X_val   = np.load(os.path.join(FEATURE_DIR, "X_val.npy"))
y_val   = np.load(os.path.join(FEATURE_DIR, "y_val.npy"))
X_test  = np.load(os.path.join(FEATURE_DIR, "X_test.npy"))
y_test  = np.load(os.path.join(FEATURE_DIR, "y_test.npy"))

print(f"  Train : {X_train.shape}  Val : {X_val.shape}  Test : {X_test.shape}")
print_memory("after load")


# ── 2. Load scaler saved during feature extraction ────────────
print("\n[2/5] Loading saved scaler …")
scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")

if os.path.exists(scaler_path):
    scaler = joblib.load(scaler_path)
    print(f"  Loaded scaler from: {scaler_path}")
else:
    from sklearn.preprocessing import StandardScaler
    print("  WARNING: no saved scaler found — fitting a new one.")
    print(f"  Expected scaler at: {scaler_path}")
    print("  Re-run feature_extractor_efficientnet.py to generate a consistent scaler.")
    scaler = StandardScaler()
    scaler.fit(X_train)
    joblib.dump(scaler, scaler_path)

X_train = scaler.transform(X_train)
X_val   = scaler.transform(X_val)
X_test  = scaler.transform(X_test)
print_memory("after scaling")


# ── 3. Build model — Run 376 config ───────────────────────────
print("\n[3/5] Building model …")

input_dim = X_train.shape[1]   # 1287 = 1280 EfficientNetB0 + 7 colour features
reg       = l1_l2(l1=L1_REG, l2=L2_REG)

model = Sequential([
    Input(shape=(input_dim,)),

    # Block 1 — 64 neurons, sigmoid, dropout 0.5
    Dense(NEURONS_L1, kernel_regularizer=reg),
    BatchNormalization(),
    Activation(ACTIVATION),
    Dropout(DROPOUT_L1),

    # Block 2 — 128 neurons, sigmoid, dropout 0.4
    Dense(NEURONS_L2, kernel_regularizer=reg),
    BatchNormalization(),
    Activation(ACTIVATION),
    Dropout(DROPOUT_L2),

    # Output — binary classification
    Dense(1, activation='sigmoid')
], name="banana_ann_run376")

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=[
        'accuracy',
        Precision(name='precision'),
        Recall(name='recall'),
        AUC(name='auc_pr', curve='PR'),
    ]
)

print(f"  Input dim     : {input_dim}")
print(f"  Neurons       : {NEURONS_L1} → {NEURONS_L2}")
print(f"  Activation    : {ACTIVATION}")
print(f"  L1 / L2 Reg   : {L1_REG} / {L2_REG}")
print(f"  Learning Rate : {LEARNING_RATE}")
print(f"  Dropout       : {DROPOUT_L1} (L1)  {DROPOUT_L2} (L2)")
print(f"  Batch Size    : {BATCH_SIZE}")
print(f"  Max Epochs    : {MAX_EPOCHS}")
model.summary()

total_params = (
    (input_dim * NEURONS_L1) + NEURONS_L1 +
    4 * NEURONS_L1 +
    (NEURONS_L1 * NEURONS_L2) + NEURONS_L2 +
    4 * NEURONS_L2 +
    NEURONS_L2 + 1
)
print(f"  Expected params: {total_params:,}  ({total_params/1000:.1f}K)")
print_memory("after model build")


# ── 4. Train ──────────────────────────────────────────────────
print("\n[4/5] Training …")

callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=ES_PATIENCE,
        restore_best_weights=True,
        verbose=1,
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=LR_PATIENCE,
        min_lr=1e-6,
        verbose=1,
    ),
]

print_memory("before training")

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=MAX_EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1,
)

actual_epochs = len(history.history['loss'])
print(f"\n  Stopped at epoch: {actual_epochs} / {MAX_EPOCHS}")
print_memory("after training")


# ── 5. Evaluate ───────────────────────────────────────────────
print("\n[5/5] Evaluating …")

def evaluate_split(name, X, y):
    results      = model.evaluate(X, y, verbose=0)
    metric_names = [m.name for m in model.metrics]
    print(f"\n  {name}")
    for n, v in zip(metric_names, results):
        print(f"    {n:12s}: {v:.4f}")

evaluate_split("Train", X_train, y_train)
evaluate_split("Val",   X_val,   y_val)
evaluate_split("Test",  X_test,  y_test)
print_memory("after evaluation")

# Detailed classification report
y_pred = (model.predict(X_test, verbose=0) > 0.5).astype("int32")

# Load classes from models/efficientnet/classes.npy
classes_path = os.path.join(CLASSES_DIR, "classes.npy")
if os.path.exists(classes_path):
    classes = np.load(classes_path, allow_pickle=True).tolist()
else:
    print(f"  WARNING: classes.npy not found at {classes_path}")
    print("  Using default labels: ['natural', 'artificial']")
    classes = ['natural', 'artificial']

print("\n  Test classification report:")
print(classification_report(y_test, y_pred, target_names=classes))

# Gap analysis
train_res = model.evaluate(X_train, y_train, verbose=0)
val_res   = model.evaluate(X_val,   y_val,   verbose=0)
gap       = val_res[1] - train_res[1]
print(f"\n  Val vs Train Gap : {gap:.4f}  "
      f"({'slight overfit — normal' if abs(gap) <= 0.03 else 'check for overfit'})")
print_memory("after prediction")


# ── Save ──────────────────────────────────────────────────────
model_path  = os.path.join(OUTPUT_DIR, "ann_classifier.keras")
scaler_save = os.path.join(OUTPUT_DIR, "scaler.pkl")

model.save(model_path)
joblib.dump(scaler, scaler_save)

print(f"\n  Model saved  → {model_path}")
print(f"  Scaler saved → {scaler_save}")

size_mb = os.path.getsize(model_path) / (1024 ** 2)
print(f"  Model size   : {size_mb:.2f} MB")
print_memory("after save")

print("\n" + "="*55)
print("  Expected results (from Run 376):")
print("    Val Accuracy  : 0.9802")
print("    Test Accuracy : 0.9837")
print("    Precision     : 0.9879")
print("    Recall        : 0.9794")
print("    F1 Score      : 0.9836")
print("="*55)