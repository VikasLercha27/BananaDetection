import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input

# ----------------------------
# CONFIG
# ----------------------------
DATASET_PATH = "D:\\mango_detection\\venv\\dataset"
FEATURE_DIR = "features/vgg16"
os.makedirs(FEATURE_DIR, exist_ok=True)

classes = ["natural", "artificial"]

# ----------------------------
# LOAD CNN (ONCE)
# ----------------------------
cnn = VGG16(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3),
    pooling="avg"
)

# ----------------------------
# IMAGE PREPROCESS
# ----------------------------
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

# ----------------------------
# COLOR FEATURES
# ----------------------------
def extract_color_features(img_rgb):

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

# ----------------------------
# CNN FEATURES
# ----------------------------
def extract_cnn_features(img):

    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    return cnn.predict(img, verbose=0).squeeze()

# ----------------------------
# BUILD FEATURES
# ----------------------------
def build_features(paths, labels):

    X, y = [], []

    for path, label in zip(paths, labels):

        img = preprocess_image(path)
        if img is None:
            continue

        cnn_feat = extract_cnn_features(img)
        color_feat = extract_color_features(img)

        X.append(np.concatenate([cnn_feat, color_feat]))
        y.append(label)

    return np.array(X), np.array(y)

# ----------------------------
# RUN SCRIPT
# ----------------------------
if __name__ == "__main__":

    print("Feature extraction started")

    image_paths, labels = [], []

    for label, cls in enumerate(classes):
        folder = os.path.join(DATASET_PATH, cls)

        for file in os.listdir(folder):
            image_paths.append(os.path.join(folder, file))
            labels.append(label)

    image_paths = np.array(image_paths)
    labels = np.array(labels)

    train_paths, temp_paths, y_train, y_temp = train_test_split(
        image_paths, labels,
        test_size=0.3,
        stratify=labels,
        random_state=42
    )

    val_paths, test_paths, y_val, y_test = train_test_split(
        temp_paths, y_temp,
        test_size=0.5,
        stratify=y_temp,
        random_state=42
    )

    print("Extracting train features...")
    X_train, y_train = build_features(train_paths, y_train)

    print("Extracting val features...")
    X_val, y_val = build_features(val_paths, y_val)

    print("Extracting test features...")
    X_test, y_test = build_features(test_paths, y_test)

    np.save(f"{FEATURE_DIR}/X_train.npy", X_train)
    np.save(f"{FEATURE_DIR}/y_train.npy", y_train)

    np.save(f"{FEATURE_DIR}/X_val.npy", X_val)
    np.save(f"{FEATURE_DIR}/y_val.npy", y_val)

    np.save(f"{FEATURE_DIR}/X_test.npy", X_test)
    np.save(f"{FEATURE_DIR}/y_test.npy", y_test)

    np.save("models/vgg16/classes.npy", np.array(classes))

    print("Feature extraction completed and saved")