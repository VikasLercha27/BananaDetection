print("Training SVC classifier")

BACKBONE = "vgg16"   # change to "vgg16" when needed

import numpy as np
import joblib
import psutil
import os

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


# ----------------------------
# DIRECTORIES
# ----------------------------
FEATURE_DIR = f"features/{BACKBONE}"
MODEL_DIR = f"models/{BACKBONE}"

os.makedirs(MODEL_DIR, exist_ok=True)


# ----------------------------
# MEMORY FUNCTION
# ----------------------------
def print_memory(stage):
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / (1024 * 1024)  # MB
    print(f"[{stage}] RAM Usage: {memory:.2f} MB")


print_memory("Start")


# ----------------------------
# LOAD FEATURES
# ----------------------------
X_train = np.load(f"{FEATURE_DIR}/X_train.npy")
y_train = np.load(f"{FEATURE_DIR}/y_train.npy")

X_val = np.load(f"{FEATURE_DIR}/X_val.npy")
y_val = np.load(f"{FEATURE_DIR}/y_val.npy")

X_test = np.load(f"{FEATURE_DIR}/X_test.npy")
y_test = np.load(f"{FEATURE_DIR}/y_test.npy")

print("Features loaded")
print_memory("After Loading Data")


# ----------------------------
# SCALE FEATURES
# ----------------------------
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

print_memory("After Scaling")


# ----------------------------
# BUILD CLASSIFIER
# ----------------------------
clf = SVC(kernel="linear", C=0.5, probability=True)

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
n_support_vectors = clf.support_vectors_.shape[0]
n_features = clf.support_vectors_.shape[1]

weight_params = n_support_vectors * n_features
bias_params = 1

total_params = weight_params + bias_params

print("\n----- SVM Parameters -----")
print("Number of Support Vectors:", n_support_vectors)
print("Number of Features:", n_features)
print("Weight Parameters:", weight_params)
print("Bias Parameters:", bias_params)
print("Total Parameters:", total_params)

# ----------------------------
# EVALUATION
# ----------------------------
print("Train Accuracy:", accuracy_score(y_train, clf.predict(X_train)))
print("Val Accuracy:", accuracy_score(y_val, clf.predict(X_val)))
print("Test Accuracy:", accuracy_score(y_test, clf.predict(X_test)))

print_memory("After Evaluation")

print("\nTest Classification Report:")
print(classification_report(y_test, clf.predict(X_test)))


# ----------------------------
# SAVE MODEL
# ----------------------------
joblib.dump(clf, f"{MODEL_DIR}/svm_classifier.pkl")
joblib.dump(scaler, f"{MODEL_DIR}/feature_scaler.pkl")

print("Model and scaler saved")

print_memory("After Saving Model")


# ----------------------------
# MODEL SIZE ON DISK
# ----------------------------
size = os.path.getsize(f"{MODEL_DIR}/svm_classifier.pkl") / (1024 * 1024)
print(f"SVC model size: {size:.2f} MB")