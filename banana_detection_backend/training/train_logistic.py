print("Training Logistic Regression classifier")

BACKBONE = "vgg16"   # change to "efficientnet", "mobilenet", "resnet" when needed

import numpy as np
import joblib
import psutil
import os

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score


# ----------------------------
# DIRECTORIES
# ----------------------------
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURE_DIR = os.path.join(BASE_DIR, "features_model", BACKBONE)       # X_train/val/test .npy files
MODEL_DIR   = os.path.join(BASE_DIR, "features_classifier", BACKBONE)  # save model + scaler here

os.makedirs(MODEL_DIR, exist_ok=True)


# ----------------------------
# MEMORY FUNCTION
# ----------------------------
def print_memory(stage):
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / (1024 * 1024)
    print(f"[{stage}] RAM Usage: {memory:.2f} MB")


print_memory("Start")


# ----------------------------
# LOAD FEATURES
# ----------------------------
X_train = np.load(os.path.join(FEATURE_DIR, "X_train.npy"))
y_train = np.load(os.path.join(FEATURE_DIR, "y_train.npy"))

X_val = np.load(os.path.join(FEATURE_DIR, "X_val.npy"))
y_val = np.load(os.path.join(FEATURE_DIR, "y_val.npy"))

X_test = np.load(os.path.join(FEATURE_DIR, "X_test.npy"))
y_test = np.load(os.path.join(FEATURE_DIR, "y_test.npy"))

print("Features loaded")
print_memory("After Loading Data")


# ----------------------------
# SCALE FEATURES
# ----------------------------
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)
X_test  = scaler.transform(X_test)

print_memory("After Scaling")


# ----------------------------
# BUILD CLASSIFIER
# ----------------------------
clf = LogisticRegression(
    C=0.01,
    max_iter=1000,
    solver="lbfgs"
)

print_memory("After Model Creation")


# ----------------------------
# TRAIN CLASSIFIER
# ----------------------------
print_memory("Before Training")

clf.fit(X_train, y_train)

print_memory("After Training")

# ----------------------------
# PARAMETER COUNT
# ----------------------------
n_features = X_train.shape[1]
n_classes  = len(clf.classes_)

weight_params = n_features * n_classes
bias_params   = n_classes
total_params  = weight_params + bias_params

print("\n----- Logistic Regression Parameters -----")
print("Number of Features:", n_features)
print("Number of Classes:", n_classes)
print("Weight Parameters:", weight_params)
print("Bias Parameters:", bias_params)
print("Total Parameters:", total_params)

# ----------------------------
# EVALUATION
# ----------------------------
train_pred = clf.predict(X_train)
val_pred   = clf.predict(X_val)
test_pred  = clf.predict(X_test)

print("Train Accuracy:", accuracy_score(y_train, train_pred))
print("Val Accuracy:",   accuracy_score(y_val,   val_pred))
print("Test Accuracy:",  accuracy_score(y_test,  test_pred))

print_memory("After Evaluation")

print("\nTest Classification Report:")
print(classification_report(y_test, test_pred))

# ROC-AUC
test_prob = clf.predict_proba(X_test)[:, 1]
print("Test ROC-AUC:", roc_auc_score(y_test, test_prob))


# ----------------------------
# SAVE MODEL
# ----------------------------
model_path  = os.path.join(MODEL_DIR, "logistic_classifier.pkl")
scaler_path = os.path.join(MODEL_DIR, "feature_scaler.pkl")

joblib.dump(clf,    model_path)
joblib.dump(scaler, scaler_path)

print(f"Model saved  → {model_path}")
print(f"Scaler saved → {scaler_path}")

print_memory("After Saving Model")


# ----------------------------
# MODEL SIZE ON DISK
# ----------------------------
size = os.path.getsize(model_path) / (1024 * 1024)
print(f"Logistic model size: {size:.2f} MB")