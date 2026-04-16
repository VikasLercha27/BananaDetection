# ============================================================
# explainable_ai.py — XAI for Mango Detection ANN
#
# Methods:
#   1. SHAP — feature importance on 1287-dim feature vectors
#   2. Grad-CAM — heatmap on original images via EfficientNet
#   3. LIME — superpixel explanation on original images
#   4. Prediction confidence analysis
#
# pip install shap lime matplotlib numpy tensorflow joblib
# ============================================================

print("Running Explainable AI analysis …")

BACKBONE = "efficientnet"

import os
import numpy as np
import joblib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import (
    Dense, Dropout, BatchNormalization,
    Activation, Input
)
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image as keras_image
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

FEATURE_DIR = f"features/{BACKBONE}"
MODEL_DIR   = f"models/{BACKBONE}"
OUTPUT_DIR  = "xai_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Rebuild model architecture (Run 376 config) ───────────────
NEURONS_L1    = 64
NEURONS_L2    = 32
ACTIVATION    = 'relu'
L1_REG        = 0.001
L2_REG        = 0.001
LEARNING_RATE = 0.0005
DROPOUT_L1    = 0.3
DROPOUT_L2    = 0.2

# ── Helpers ───────────────────────────────────────────────────
def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ════════════════════════════════════════════════════════════════
# STEP 1 — Load everything
# ════════════════════════════════════════════════════════════════
print_section("1 / 4  Loading model, scaler and features")

scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
classes = np.load(f"{MODEL_DIR}/classes.npy", allow_pickle=True).tolist()
print(f"  Classes : {classes}")

X_train_raw = np.load(f"{FEATURE_DIR}/X_train.npy")
X_test_raw  = np.load(f"{FEATURE_DIR}/X_test.npy")
y_train     = np.load(f"{FEATURE_DIR}/y_train.npy")
y_test      = np.load(f"{FEATURE_DIR}/y_test.npy")

X_train = scaler.transform(X_train_raw)
X_test  = scaler.transform(X_test_raw)

input_dim = X_train.shape[1]
print(f"  Feature dim : {input_dim}")
print(f"  Test samples: {len(X_test)}")

# Load trained model
model_path = f"{MODEL_DIR}/ann_classifier.keras"
if os.path.exists(model_path):
    model = load_model(model_path)
    print(f"  Loaded model from {model_path}")
else:
    # Rebuild if .keras not found
    print("  Rebuilding model from scratch …")
    reg = l1_l2(l1=L1_REG, l2=L2_REG)
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(NEURONS_L1, kernel_regularizer=reg),
        BatchNormalization(), Activation(ACTIVATION), Dropout(DROPOUT_L1),
        Dense(NEURONS_L2, kernel_regularizer=reg),
        BatchNormalization(), Activation(ACTIVATION), Dropout(DROPOUT_L2),
        Dense(1, activation='sigmoid')
    ], name="mango_ann_run376")
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    print("  WARNING: Model not trained — load weights or train first.")

# Predictions on test set
y_pred_prob = model.predict(X_test, verbose=0).flatten()
y_pred      = (y_pred_prob >= 0.5).astype(int)

print(f"\n  Test Accuracy : {np.mean(y_pred == y_test):.4f}")
print(f"\n  Classification Report:")
print(classification_report(y_test, y_pred, target_names=classes))


# ════════════════════════════════════════════════════════════════
# STEP 2 — SHAP Analysis
# ════════════════════════════════════════════════════════════════
print_section("2 / 4  SHAP — Feature Importance")

try:
    import shap

    # Use a background sample from training data
    background  = X_train[np.random.choice(len(X_train), 100, replace=False)]
    test_sample = X_test[:50]

    print("  Computing SHAP values (this may take 1–2 mins) …")
    explainer   = shap.DeepExplainer(model, background)
    shap_values = explainer.shap_values(test_sample)

    # shap_values shape depends on TF version — flatten if needed
    if isinstance(shap_values, list):
        sv = shap_values[0]
    else:
        sv = shap_values
    if sv.ndim == 3:
        sv = sv[:, :, 0]

    # ── Plot 1: Summary bar — top 20 most important features ───
    fig, ax = plt.subplots(figsize=(10, 7))
    shap.summary_plot(sv, test_sample,
                      plot_type="bar",
                      max_display=20,
                      show=False)
    plt.title("SHAP — Top 20 Most Important Features\n(mean absolute SHAP value)",
              fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/shap_summary_bar.png",
                bbox_inches='tight', dpi=130)
    plt.close()
    print("  Saved: xai_outputs/shap_summary_bar.png")

    # ── Plot 2: Summary dot — feature impact direction ──────────
    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(sv, test_sample,
                      max_display=20,
                      show=False)
    plt.title("SHAP — Feature Impact Direction\n(red=pushes toward mango, blue=pushes away)",
              fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/shap_summary_dot.png",
                bbox_inches='tight', dpi=130)
    plt.close()
    print("  Saved: xai_outputs/shap_summary_dot.png")

    # ── Plot 3: Waterfall for single predictions ─────────────────
    # Find one correct mango, one correct natural, one wrong prediction
    correct_mango   = np.where((y_pred == 1) & (y_test == 1))[0]
    correct_natural = np.where((y_pred == 0) & (y_test == 0))[0]
    wrong_preds     = np.where(y_pred != y_test)[0]

    sample_indices = {}
    if len(correct_mango)   > 0: sample_indices['Correct — Mango']   = correct_mango[0]
    if len(correct_natural) > 0: sample_indices['Correct — Natural']  = correct_natural[0]
    if len(wrong_preds)     > 0: sample_indices['Wrong Prediction']   = wrong_preds[0]

    # Fix base_values — convert scalar tensor to plain float safely
    raw_base = explainer.expected_value
    if isinstance(raw_base, list):
        base_val = float(raw_base[0])
    elif hasattr(raw_base, "numpy"):
        base_val = float(np.array(raw_base).flatten()[0])
    else:
        base_val = float(np.array(raw_base).flatten()[0])

    for label, idx in sample_indices.items():
        if idx < len(sv):
            exp = shap.Explanation(
                values        = sv[idx],
                base_values   = base_val,
                data          = test_sample[idx],
                feature_names = [f"Feature {i}" for i in range(input_dim)]
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            shap.waterfall_plot(exp, max_display=15, show=False)
            pred_class = classes[y_pred[idx]]
            true_class = classes[y_test[idx]]
            conf       = y_pred_prob[idx] if y_pred[idx] == 1 else 1 - y_pred_prob[idx]
            plt.title(f"SHAP Waterfall — {label}\n"
                      f"Predicted: {pred_class} ({conf:.2%})  |  "
                      f"True: {true_class}",
                      fontsize=11, fontweight='bold')
            plt.tight_layout()
            fname = label.lower().replace(' ', '_').replace('—', '').replace('  ', '_')
            plt.savefig(f"{OUTPUT_DIR}/shap_waterfall_{fname}.png",
                        bbox_inches='tight', dpi=130)
            plt.close()
            print(f"  Saved: xai_outputs/shap_waterfall_{fname}.png")

    # ── Plot 4: Global feature importance ranking ────────────────
    mean_abs_shap = np.abs(sv).mean(axis=0)
    top20_idx     = np.argsort(mean_abs_shap)[::-1][:20]
    top20_vals    = mean_abs_shap[top20_idx]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF5722' if v > top20_vals.mean() else '#2196F3'
              for v in top20_vals]
    bars = ax.barh([f"Feature {i}" for i in top20_idx[::-1]],
                   top20_vals[::-1], color=colors[::-1], alpha=0.85)
    ax.set_xlabel("Mean |SHAP value|", fontsize=11)
    ax.set_title("Top 20 Features by Global SHAP Importance\n"
                 "(orange = above average importance)",
                 fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, top20_vals[::-1]):
        ax.text(bar.get_width() + 0.0001, bar.get_y() + bar.get_height()/2,
                f'{val:.4f}', va='center', fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/shap_feature_ranking.png",
                bbox_inches='tight', dpi=130)
    plt.close()
    print("  Saved: xai_outputs/shap_feature_ranking.png")

except ImportError:
    print("  SHAP not installed. Run: pip install shap")
except Exception as e:
    print(f"  SHAP error: {e}")


# ════════════════════════════════════════════════════════════════
# STEP 3 — Grad-CAM on original images via EfficientNet backbone
# ════════════════════════════════════════════════════════════════
print_section("3 / 4  Grad-CAM — Visual Heatmaps on Original Images")

# NOTE: Grad-CAM works on the CNN backbone (EfficientNet), NOT the ANN.
# It shows which region of the raw image the CNN focused on
# when extracting the features your ANN classified.

IMAGE_DIR = "dataset"   # ← change to your actual image folder path
                         #   expected structure: dataset/natural/  dataset/artificial/

def get_gradcam_heatmap(backbone_model, img_array, last_conv_layer_name):
    """Generate Grad-CAM heatmap for a given image."""
    grad_model = Model(
        inputs  = backbone_model.input,
        outputs = [backbone_model.get_layer(last_conv_layer_name).output,
                   backbone_model.output]
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        # Use max activation across output channels
        loss = tf.reduce_mean(predictions)

    grads      = tape.gradient(loss, conv_outputs)
    pooled     = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out   = conv_outputs[0]
    heatmap    = conv_out @ pooled[..., tf.newaxis]
    heatmap    = tf.squeeze(heatmap)
    heatmap    = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()

def overlay_heatmap(heatmap, original_img, alpha=0.4):
    """Overlay Grad-CAM heatmap on original image."""
    import cv2
    heatmap_resized = cv2.resize(heatmap,
                                  (original_img.shape[1], original_img.shape[0]))
    heatmap_colored = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_colored, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay = (heatmap_colored * alpha + original_img * (1 - alpha)).astype(np.uint8)
    return overlay, heatmap_resized

try:
    import cv2

    # Load EfficientNet backbone
    backbone = EfficientNetB0(weights='imagenet', include_top=False,
                               pooling='avg', input_shape=(224, 224, 3))
    last_conv = 'top_conv'   # last conv layer in EfficientNetB0

    # Collect sample images from dataset folder
    sample_images = []
    if os.path.exists(r"D:\mango_detection\venv\dataset"):
        for class_name in classes:
            class_dir = os.path.join(r"D:\mango_detection\venv\dataset", class_name)
            if os.path.exists(class_dir):
                imgs = [f for f in os.listdir(class_dir)
                        if f.lower().endswith(('.jpg','.jpeg','.png'))]
                for img_name in imgs[:3]:   # 3 samples per class
                    sample_images.append({
                        'path'  : os.path.join(class_dir, img_name),
                        'label' : class_name
                    })

    if sample_images:
        n_imgs = len(sample_images)
        fig, axes = plt.subplots(n_imgs, 3,
                                  figsize=(12, 4 * n_imgs))
        if n_imgs == 1:
            axes = [axes]
        fig.suptitle("Grad-CAM — Where EfficientNet Looks\n"
                     "(Original | Heatmap | Overlay)",
                     fontsize=14, fontweight='bold')

        for row_idx, sample in enumerate(sample_images):
            # Load and preprocess image
            img_orig    = keras_image.load_img(sample["path"], target_size=(224, 224))
            img_array   = keras_image.img_to_array(img_orig)
            img_orig_np = img_array.astype(np.uint8)
            img_input   = tf.keras.applications.efficientnet.preprocess_input(
                img_array[np.newaxis, ...]
            )

            # Generate heatmap
            heatmap = get_gradcam_heatmap(backbone, img_input, last_conv)
            overlay, heatmap_resized = overlay_heatmap(heatmap, img_orig_np)

            # ── Get ANN prediction ──────────────────────────────────────
            # Extract backbone features (1280-dim)
            eff_feat = backbone.predict(img_input, verbose=0)   # (1, 1280)

            # Extract EXACT same 7 colour features as extract_features.py:
            # [mean_H, std_H, mean_S, std_S, mean_V, mean_A, mean_B]
            hsv = cv2.cvtColor(img_orig_np, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)
            lab = cv2.cvtColor(img_orig_np, cv2.COLOR_RGB2LAB)
            l_ch, a_ch, b_ch = cv2.split(lab)
            colour_feat = np.array([[
                np.mean(h), np.std(h),
                np.mean(s), np.std(s),
                np.mean(v),
                np.mean(a_ch), np.mean(b_ch)
            ]])  # (1, 7) — matches extract_features.py exactly

            # Concatenate: 1280 (EfficientNet) + 7 (colour) = 1287
            full_feat   = np.concatenate([eff_feat, colour_feat], axis=1)
            feat_scaled = scaler.transform(full_feat)
            prob        = model.predict(feat_scaled, verbose=0)[0][0]
            pred_class  = classes[int(prob >= 0.5)]
            conf        = prob if prob >= 0.5 else 1 - prob

            ax_row = axes[row_idx] if n_imgs > 1 else axes

            ax_row[0].imshow(img_orig_np)
            ax_row[0].set_title(f"Original\nTrue: {sample['label']}",
                                 fontsize=10, fontweight='bold')
            ax_row[0].axis('off')

            ax_row[1].imshow(heatmap_resized, cmap='jet')
            ax_row[1].set_title("Grad-CAM Heatmap\n(red = high attention)",
                                 fontsize=10)
            ax_row[1].axis('off')

            ax_row[2].imshow(overlay)
            ax_row[2].set_title(f"Overlay\nPred: {pred_class} ({conf:.1%})",
                                 fontsize=10,
                                 color='green' if pred_class == sample['label']
                                               else 'red')
            ax_row[2].axis('off')

        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/gradcam_heatmaps.png",
                    bbox_inches='tight', dpi=130)
        plt.close()
        print("  Saved: xai_outputs/gradcam_heatmaps.png")

    else:
        print(f"  No images found in '{IMAGE_DIR}' folder.")
        print("  Change IMAGE_DIR variable to your dataset path.")
        print("  Expected: dataset/natural/img1.jpg, dataset/artificial/img1.jpg")

except ImportError:
    print("  OpenCV not installed. Run: pip install opencv-python")
except Exception as e:
    print(f"  Grad-CAM error: {e}")


# ════════════════════════════════════════════════════════════════
# STEP 4 — Prediction Confidence Analysis
# ════════════════════════════════════════════════════════════════
print_section("4 / 4  Prediction Confidence Analysis")

# ── Plot 1: Confidence distribution ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Prediction Confidence Analysis", fontsize=14, fontweight='bold')

# Confidence histogram per true class
for cls_idx, cls_name in enumerate(classes):
    mask  = y_test == cls_idx
    probs = y_pred_prob[mask]
    conf  = np.where(cls_idx == 1, probs, 1 - probs)
    color = '#FF5722' if cls_idx == 1 else '#2196F3'
    axes[0].hist(conf, bins=25, alpha=0.65,
                 color=color, label=cls_name, density=True)

axes[0].axvline(x=0.5,  color='black', linewidth=1.2,
                linestyle='--', alpha=0.5, label='0.5 threshold')
axes[0].axvline(x=0.9,  color='green', linewidth=1.0,
                linestyle=':', alpha=0.5, label='0.9 high confidence')
axes[0].set_xlabel("Prediction Confidence", fontsize=11)
axes[0].set_ylabel("Density", fontsize=11)
axes[0].set_title("Confidence Distribution per Class", fontsize=11, fontweight='bold')
axes[0].legend(fontsize=9)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# ── Plot 2: Correct vs Wrong prediction confidence ───────────────
correct_conf = y_pred_prob[y_pred == y_test]
correct_conf = np.where(y_pred[y_pred == y_test] == 1,
                         correct_conf, 1 - correct_conf)
wrong_conf   = y_pred_prob[y_pred != y_test]
wrong_conf   = np.where(y_pred[y_pred != y_test] == 1,
                         wrong_conf, 1 - wrong_conf)

axes[1].hist(correct_conf, bins=25, alpha=0.65,
             color='#4CAF50', label=f'Correct ({len(correct_conf)})', density=True)
if len(wrong_conf) > 0:
    axes[1].hist(wrong_conf, bins=15, alpha=0.65,
                 color='#F44336', label=f'Wrong ({len(wrong_conf)})', density=True)

axes[1].axvline(x=0.5, color='black', linewidth=1.2,
                linestyle='--', alpha=0.5)
axes[1].set_xlabel("Prediction Confidence", fontsize=11)
axes[1].set_ylabel("Density", fontsize=11)
axes[1].set_title("Correct vs Wrong Predictions\nby Confidence Level",
                   fontsize=11, fontweight='bold')
axes[1].legend(fontsize=9)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/confidence_analysis.png",
            bbox_inches='tight', dpi=130)
plt.close()
print("  Saved: xai_outputs/confidence_analysis.png")

# ── Plot 3: Most confident correct & most uncertain predictions ──
confidence_all = np.where(y_pred == 1, y_pred_prob, 1 - y_pred_prob)

# Top 10 most confident correct predictions
correct_mask  = y_pred == y_test
correct_idx   = np.where(correct_mask)[0]
top_correct   = correct_idx[np.argsort(confidence_all[correct_mask])[::-1][:10]]

# Top 10 most uncertain (closest to 0.5)
uncertainty   = np.abs(y_pred_prob - 0.5)
uncertain_idx = np.argsort(uncertainty)[:10]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Confidence Extremes", fontsize=14, fontweight='bold')

# Most confident
x1 = np.arange(len(top_correct))
colors_conf = ['#4CAF50' if y_pred[i] == y_test[i] else '#F44336'
               for i in top_correct]
axes[0].bar(x1, confidence_all[top_correct], color=colors_conf, alpha=0.85)
axes[0].set_xticks(x1)
axes[0].set_xticklabels([f"#{i}\n{classes[y_pred[i]]}" for i in top_correct],
                          fontsize=7.5, rotation=30, ha='right')
axes[0].set_ylabel("Confidence", fontsize=11)
axes[0].set_ylim(0.9, 1.005)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.3f}'))
axes[0].set_title("Top 10 Most Confident Correct Predictions",
                   fontsize=11, fontweight='bold')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].axhline(y=0.97, color='navy', linewidth=1,
                linestyle='--', alpha=0.4)

# Most uncertain
x2 = np.arange(len(uncertain_idx))
colors_unc = ['#4CAF50' if y_pred[i] == y_test[i] else '#F44336'
              for i in uncertain_idx]
axes[1].bar(x2, confidence_all[uncertain_idx], color=colors_unc, alpha=0.85)
axes[1].set_xticks(x2)
axes[1].set_xticklabels([f"#{i}\n{classes[y_pred[i]]}" for i in uncertain_idx],
                          fontsize=7.5, rotation=30, ha='right')
axes[1].set_ylabel("Confidence", fontsize=11)
axes[1].set_ylim(0, 0.7)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.3f}'))
axes[1].set_title("Top 10 Most Uncertain Predictions\n(green=correct, red=wrong)",
                   fontsize=11, fontweight='bold')
axes[1].axhline(y=0.5, color='black', linewidth=1.2,
                linestyle='--', alpha=0.4, label='0.5 boundary')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/confidence_extremes.png",
            bbox_inches='tight', dpi=130)
plt.close()
print("  Saved: xai_outputs/confidence_extremes.png")

# ── Summary stats ────────────────────────────────────────────────
print(f"\n  === Confidence Summary ===")
print(f"  Mean confidence (correct) : {correct_conf.mean():.4f}")
wrong_conf_str = f"{wrong_conf.mean():.4f}" if len(wrong_conf) > 0 else "N/A"
print(f"  Mean confidence (wrong)   : {wrong_conf_str}")
print(f"  Predictions > 90% conf    : {(confidence_all > 0.9).sum()} / {len(confidence_all)}"
      f"  ({(confidence_all > 0.9).mean():.1%})")
print(f"  Predictions > 95% conf    : {(confidence_all > 0.95).sum()} / {len(confidence_all)}"
      f"  ({(confidence_all > 0.95).mean():.1%})")
print(f"  Uncertain (40–60% conf)   : {((confidence_all > 0.4) & (confidence_all < 0.6)).sum()}")

print(f"\n{'='*60}")
print(f"  XAI Analysis Complete!")
print(f"  All outputs saved in: xai_outputs/")
print(f"    shap_summary_bar.png       — top 20 features (bar)")
print(f"    shap_summary_dot.png       — feature impact direction")
print(f"    shap_waterfall_*.png       — per-sample explanations")
print(f"    shap_feature_ranking.png   — global importance ranking")
print(f"    gradcam_heatmaps.png       — visual heatmaps on images")
print(f"    confidence_analysis.png    — confidence distributions")
print(f"    confidence_extremes.png    — most/least confident runs")
print(f"{'='*60}")