// import { PREDICTION_URL } from "../config/api";

// export const submitImageForPrediction = async (
//   imageUri,
//   selectedModel = "ann_classifier"
// ) => {

//   const filename = imageUri.split("/").pop() || "image.jpg";

//   const match = /\.(\w+)$/.exec(filename);
//   const type = match ? `image/${match[1]}` : `image`;

//   const formData = new FormData();

//   formData.append("image", {
//     uri: imageUri,
//     name: filename,
//     type: type,
//   });

//   formData.append("model", selectedModel);

//   const response = await fetch(PREDICTION_URL, {
//     method: "POST",
//     body: formData,
//   });

//   if (!response.ok) {
//     const text = await response.text();
//     console.log("SERVER ERROR:", text);
//     throw new Error(`Upload failed: ${response.status}`);
//   }

//   return response.json();
// };
import { PREDICTION_URL } from "../config/api";

/**
 * Sends an image to the FastAPI backend for prediction.
 * EfficientNetB0 + ANN is the only model now.
 *
 * @param {string} imageUri  - local URI of the image
 * @returns {Promise<object>} - { label, confidence, prediction, model, backbone, raw_prob }
 */
export const submitImageForPrediction = async (imageUri) => {

  const filename = imageUri.split("/").pop() || "image.jpg";
  const match    = /\.(\w+)$/.exec(filename);
  const type     = match ? `image/${match[1].toLowerCase()}` : "image/jpeg";

  const formData = new FormData();
  formData.append("image", { uri: imageUri, name: filename, type });
  formData.append("model", "ann_classifier");   // only model available

  const response = await fetch(PREDICTION_URL, {
    method : "POST",
    body   : formData,
    // Do NOT set Content-Type header manually —
    // React Native sets it automatically with the correct boundary
  });

  if (!response.ok) {
    const text = await response.text();
    console.error("SERVER ERROR:", text);
    throw new Error(`Server error ${response.status}: ${text}`);
  }

  return response.json();
};