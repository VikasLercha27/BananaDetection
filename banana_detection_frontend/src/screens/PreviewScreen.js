// import { useState } from "react";
// import { Picker } from "@react-native-picker/picker";
// import {
//   View,
//   Image,
//   TouchableOpacity,
//   Text,
//   StyleSheet,
//   ActivityIndicator,
// } from "react-native";
// import { SafeAreaView } from "react-native-safe-area-context";
// import * as ImagePicker from "expo-image-picker";
// import AppLayout from "../components/AppLayout";
// import { submitImageForPrediction } from "../services/predictionService";

// export default function PreviewScreen({ route, navigation }) {
//   const { imageUri } = route.params;
//   const [currentImage, setCurrentImage] = useState(imageUri);
//   const [isSubmitting, setIsSubmitting] = useState(false);
//   const [errorMessage, setErrorMessage] = useState("");
//   const [selectedModel, setSelectedModel] = useState("ann_classifier");

//   // Process image
//   const handleProcess = async () => {
//     if (isSubmitting) return;

//     try {
//       setErrorMessage("");
//       setIsSubmitting(true);

//       const prediction = await submitImageForPrediction(
//         currentImage,
//         selectedModel
//       );

//       navigation.navigate("Result", {
//         imageUri: currentImage,
//         prediction,
//       });
//     } catch (error) {
//       setErrorMessage(error.message || "Unable to process image");
//     } finally {
//       setIsSubmitting(false);
//     }
//   };

//   // Open camera again
//   const openCamera = async () => {
//     const permission = await ImagePicker.requestCameraPermissionsAsync();
//     if (!permission.granted) return;

//     const result = await ImagePicker.launchCameraAsync({
//       quality: 0.7,
//     });

//     if (!result.canceled) {
//       setCurrentImage(result.assets[0].uri);
//     }
//   };

//   // Pick from gallery
//   const openGallery = async () => {
//     const permission =
//       await ImagePicker.requestMediaLibraryPermissionsAsync();
//     if (!permission.granted) return;

//     const result = await ImagePicker.launchImageLibraryAsync({
//       mediaTypes: ImagePicker.MediaTypeOptions.Images,
//       quality: 0.7,
//     });

//     if (!result.canceled) {
//       setCurrentImage(result.assets[0].uri);
//     }
//   };

//   return (
//     <AppLayout title="Preview">
//       <SafeAreaView style={styles.container}>
//         {/* Image Preview */}
//         <View style={styles.imageCard}>
//           <Image source={{ uri: currentImage }} style={styles.image} />
//         </View>

//         {/* Model Selector */}
//         <View style={styles.modelSelector}>
//           <Text style={styles.modelLabel}>Select Model</Text>

//           <Picker
//             selectedValue={selectedModel}
//             onValueChange={(itemValue) => setSelectedModel(itemValue)}
//             style={styles.picker}
//           >
//             <Picker.Item label="ANN Classifier (Default)" value="ann_classifier" />
//             <Picker.Item label="Logistic Regression" value="logistic" />
//             <Picker.Item label="SVC" value="svc" />
//           </Picker>
//         </View>

//         {/* Camera / Gallery */}
//         <View style={styles.pickBar}>
//           <TouchableOpacity style={styles.pickButton} onPress={openCamera}>
//             <Text style={styles.pickText}>📷 Camera</Text>
//           </TouchableOpacity>

//           <TouchableOpacity style={styles.pickButton} onPress={openGallery}>
//             <Text style={styles.pickText}>🖼 Gallery</Text>
//           </TouchableOpacity>
//         </View>

//         {/* Bottom Actions */}
//         <View style={styles.actionBar}>
//           <TouchableOpacity
//             style={[styles.button, styles.secondaryButton]}
//             onPress={() => navigation.goBack()}
//             disabled={isSubmitting}
//           >
//             <Text style={styles.secondaryText}>Retake</Text>
//           </TouchableOpacity>

//           <TouchableOpacity
//             style={[styles.button, styles.primaryButton]}
//             onPress={handleProcess}
//             disabled={isSubmitting}
//           >
//             {isSubmitting ? (
//               <ActivityIndicator color="#ffffff" />
//             ) : (
//               <Text style={styles.primaryText}>Process</Text>
//             )}
//           </TouchableOpacity>
//         </View>

//         {!!errorMessage && (
//           <Text style={styles.errorText}>{errorMessage}</Text>
//         )}
//       </SafeAreaView>
//     </AppLayout>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: "#F5F1E8",
//     padding: 12,
//   },

//   imageCard: {
//     flex: 1,
//     borderRadius: 24,
//     overflow: "hidden",
//   },

//   image: {
//     width: "100%",
//     height: "100%",
//     borderRadius: 24,
//     resizeMode: "cover",
//   },

//   modelSelector: {
//     marginTop: 10,
//     backgroundColor: "#FFFFFF",
//     borderRadius: 12,
//     paddingHorizontal: 10,
//   },

//   modelLabel: {
//     fontSize: 14,
//     fontWeight: "600",
//     marginTop: 6,
//     marginBottom: 4,
//   },

//   picker: {
//     width: "100%",
//   },

//   pickBar: {
//     flexDirection: "row",
//     justifyContent: "space-between",
//     marginTop: 10,
//   },

//   pickButton: {
//     flex: 1,
//     padding: 12,
//     backgroundColor: "#F59E0B",
//     borderRadius: 12,
//     marginHorizontal: 5,
//     alignItems: "center",
//   },

//   pickText: {
//     color: "white",
//     fontWeight: "600",
//   },

//   actionBar: {
//     flexDirection: "row",
//     marginTop: 16,
//   },

//   button: {
//     flex: 1,
//     paddingVertical: 14,
//     borderRadius: 12,
//     alignItems: "center",
//     justifyContent: "center",
//   },

//   primaryButton: {
//     backgroundColor: "#16A34A",
//     marginLeft: 10,
//   },

//   secondaryButton: {
//     backgroundColor: "#E5E7EB",
//     marginRight: 10,
//   },

//   primaryText: {
//     color: "#ffffff",
//     fontSize: 16,
//     fontWeight: "600",
//   },

//   secondaryText: {
//     color: "#374151",
//     fontSize: 16,
//     fontWeight: "500",
//   },

//   errorText: {
//     color: "#B91C1C",
//     marginTop: 10,
//     textAlign: "center",
//   },
// });
import { useState } from "react";
import {
  View,
  Image,
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import * as ImagePicker from "expo-image-picker";
import AppLayout from "../components/AppLayout";
import { submitImageForPrediction } from "../services/predictionService";

const MODEL_OPTIONS = [
  { label: "VGC", value: "model_a" },
  { label: "SVM", value: "model_b" },
  { label: "ANN", value: "model_c" },
];

export default function PreviewScreen({ route, navigation }) {
<<<<<<< HEAD
  const { imageUri }     = route.params;
  const [currentImage, setCurrentImage] = useState(imageUri);
  const [isSubmitting,  setIsSubmitting] = useState(false);
  const [errorMessage,  setErrorMessage] = useState("");
=======
  const { imageUri } = route.params;
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedModel, setSelectedModel] = useState(MODEL_OPTIONS[0].value);
  const [dropdownOpen, setDropdownOpen] = useState(false);
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924

  // ── Send image to FastAPI ──────────────────────────────────────
  const handleProcess = async () => {
    if (isSubmitting) return;
    try {
      setErrorMessage("");
      setIsSubmitting(true);
<<<<<<< HEAD
      const prediction = await submitImageForPrediction(currentImage);
      navigation.navigate("Result", { imageUri: currentImage, prediction });
=======
      const prediction = await submitImageForPrediction(
        imageUri,
        selectedModel,
      );
      navigation.navigate("Result", { imageUri, prediction });
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
    } catch (error) {
      setErrorMessage(error.message || "Unable to process image");
    } finally {
      setIsSubmitting(false);
    }
  };

<<<<<<< HEAD
  // ── Re-capture ─────────────────────────────────────────────────
  const openCamera = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) return;
    const result = await ImagePicker.launchCameraAsync({ quality: 0.8 });
    if (!result.canceled) setCurrentImage(result.assets[0].uri);
  };

  // ── Pick from gallery ──────────────────────────────────────────
  const openGallery = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) return;
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality   : 0.8,
    });
    if (!result.canceled) setCurrentImage(result.assets[0].uri);
  };
=======
  const selectedLabel = MODEL_OPTIONS.find(
    (m) => m.value === selectedModel,
  )?.label;
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924

  return (
    <AppLayout title="Preview">
      <SafeAreaView style={styles.container}>

        {/* Image Preview */}
        <View style={styles.imageCard}>
          <Image source={{ uri: currentImage }} style={styles.image} />

          {/* Model badge — always EfficientNet */}
          <View style={styles.modelBadge}>
            <Text style={styles.modelBadgeText}>⚡ EfficientNetB0 + ANN</Text>
          </View>
        </View>

        {/* Camera / Gallery row */}
        <View style={styles.pickBar}>
          <TouchableOpacity style={styles.pickButton} onPress={openCamera}>
            <Text style={styles.pickText}>📷  Retake</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.pickButton} onPress={openGallery}>
            <Text style={styles.pickText}>🖼  Gallery</Text>
          </TouchableOpacity>
        </View>

        {/* Actions */}
        <View style={styles.actionBar}>
          <TouchableOpacity
            style={[styles.button, styles.secondaryButton]}
            onPress={() => navigation.goBack()}
            disabled={isSubmitting}
          >
            <Text style={styles.secondaryText}>← Back</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.primaryButton]}
            onPress={handleProcess}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <View style={styles.loadingRow}>
                <ActivityIndicator color="#ffffff" size="small" />
                <Text style={[styles.primaryText, { marginLeft: 8 }]}>
                  Analysing…
                </Text>
              </View>
            ) : (
              <Text style={styles.primaryText}>🔍  Analyse</Text>
            )}
          </TouchableOpacity>
        </View>

<<<<<<< HEAD
        {!!errorMessage && (
          <Text style={styles.errorText}>⚠️  {errorMessage}</Text>
        )}

=======
        {/* Model Selector */}
        <View style={styles.modelSelectorWrapper}>
          <Text style={styles.modelLabel}>Model Type</Text>

          <TouchableOpacity
            style={styles.dropdownTrigger}
            onPress={() => setDropdownOpen((prev) => !prev)}
            activeOpacity={0.8}
          >
            <Text style={styles.dropdownTriggerText}>{selectedLabel}</Text>
            <Text style={styles.dropdownArrow}>{dropdownOpen ? "▲" : "▼"}</Text>
          </TouchableOpacity>

          {dropdownOpen && (
            <View style={styles.dropdownMenu}>
              {MODEL_OPTIONS.map((option, index) => {
                const isSelected = option.value === selectedModel;
                const isLast = index === MODEL_OPTIONS.length - 1;
                return (
                  <TouchableOpacity
                    key={option.value}
                    style={[
                      styles.dropdownItem,
                      isSelected && styles.dropdownItemSelected,
                      !isLast && styles.dropdownItemBorder,
                    ]}
                    onPress={() => {
                      setSelectedModel(option.value);
                      setDropdownOpen(false);
                    }}
                    activeOpacity={0.7}
                  >
                    <Text
                      style={[
                        styles.dropdownItemText,
                        isSelected && styles.dropdownItemTextSelected,
                      ]}
                    >
                      {option.label}
                    </Text>
                    {isSelected && <Text style={styles.checkmark}>✓</Text>}
                  </TouchableOpacity>
                );
              })}
            </View>
          )}
        </View>

        {!!errorMessage && <Text style={styles.errorText}>{errorMessage}</Text>}
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
      </SafeAreaView>
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F1E8",
    padding: 12,
  },

  imageCard: {
    flex: 1,
    borderRadius: 24,
    overflow: "hidden",
    position: "relative",
  },

  image: {
    width: "100%",
    height: "100%",
    borderRadius: 24,
    resizeMode: "cover",
  },

  modelBadge: {
    position  : "absolute",
    top       : 12,
    alignSelf : "center",
    backgroundColor: "rgba(0,0,0,0.55)",
    paddingHorizontal: 14,
    paddingVertical  : 6,
    borderRadius: 20,
  },

  modelBadgeText: {
    color     : "#FACC15",
    fontSize  : 13,
    fontWeight: "600",
  },

  pickBar: {
    flexDirection    : "row",
    justifyContent   : "space-between",
    marginTop        : 12,
  },

  pickButton: {
    flex           : 1,
    padding        : 12,
    backgroundColor: "#F59E0B",
    borderRadius   : 12,
    marginHorizontal: 5,
    alignItems     : "center",
  },

  pickText: {
    color     : "#1F2937",
    fontWeight: "700",
    fontSize  : 14,
  },

  actionBar: {
    flexDirection: "row",
    marginTop    : 14,
  },

  button: {
    flex          : 1,
    paddingVertical: 14,
    borderRadius  : 12,
    alignItems    : "center",
    justifyContent: "center",
  },
  primaryButton: {
    backgroundColor: "#16A34A",
<<<<<<< HEAD
    marginLeft     : 10,
=======
    marginLeft: 10,
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
  },

  secondaryButton: {
    backgroundColor: "#E5E7EB",
<<<<<<< HEAD
    marginRight    : 10,
=======
    marginRight: 10,
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
  },
  primaryText: {
    color     : "#ffffff",
    fontSize  : 16,
    fontWeight: "600",
  },

  secondaryText: {
    color     : "#374151",
    fontSize  : 16,
    fontWeight: "500",
  },

<<<<<<< HEAD
  loadingRow: {
    flexDirection: "row",
    alignItems   : "center",
  },

=======
  /* Model Selector */
  modelSelectorWrapper: {
    marginTop: 16,
  },
  modelLabel: {
    fontSize: 12,
    fontWeight: "600",
    color: "#6B7280",
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginBottom: 6,
  },
  dropdownTrigger: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: "#fff",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 13,
    borderWidth: 1.5,
    borderColor: "#D1FAE5",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  dropdownTriggerText: {
    fontSize: 15,
    fontWeight: "500",
    color: "#111827",
  },
  dropdownArrow: {
    fontSize: 11,
    color: "#16A34A",
    fontWeight: "600",
  },
  dropdownMenu: {
    marginTop: 6,
    backgroundColor: "#fff",
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: "#D1FAE5",
    overflow: "hidden",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 4,
  },
  dropdownItem: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 13,
  },
  dropdownItemBorder: {
    borderBottomWidth: 1,
    borderBottomColor: "#F3F4F6",
  },
  dropdownItemSelected: {
    backgroundColor: "#F0FDF4",
  },
  dropdownItemText: {
    fontSize: 15,
    color: "#374151",
  },
  dropdownItemTextSelected: {
    color: "#16A34A",
    fontWeight: "600",
  },
  checkmark: {
    color: "#16A34A",
    fontSize: 15,
    fontWeight: "700",
  },

  /* Error */
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
  errorText: {
    color    : "#B91C1C",
    marginTop: 10,
    textAlign: "center",
    fontSize : 13,
  },
});