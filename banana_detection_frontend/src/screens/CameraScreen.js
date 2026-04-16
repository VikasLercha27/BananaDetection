import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { CameraView, Camera } from "expo-camera";
import * as ImagePicker from "expo-image-picker";
import { useEffect, useRef, useState } from "react";

import AppLayout from "../components/AppLayout";

export default function CameraScreen({ navigation }) {
  const [hasPermission, setHasPermission] = useState(null);
  const cameraRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  if (hasPermission === null) {
    return <Text>Requesting camera permission...</Text>;
  }

  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  const takePicture = async () => {
    const photo = await cameraRef.current.takePictureAsync();
    navigation.navigate("Preview", { imageUri: photo.uri });
  };

  const pickFromGallery = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== "granted") {
      alert("Gallery permission is required to pick an image.");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      quality: 1,
    });

    if (!result.canceled) {
      navigation.navigate("Preview", { imageUri: result.assets[0].uri });
    }
  };

  return (
    <AppLayout title="">
      {/* Camera occupies full available space */}
      <View style={styles.cameraContainer}>
        <CameraView style={styles.camera} ref={cameraRef} facing="back" />

        {/* Overlay Text */}
        <View style={styles.overlay}>
          <Text style={styles.overlayText}>Find Banana</Text>
        </View>

        {/* Bottom Controls */}
        <View style={styles.bottomControls}>
          {/* Gallery Button */}
          <TouchableOpacity
            onPress={pickFromGallery}
            style={styles.galleryButton}
          >
            <Text style={styles.galleryIcon}>🖼️</Text>
            <Text style={styles.galleryLabel}>Gallery</Text>
          </TouchableOpacity>

          {/* Capture Button */}
          <TouchableOpacity onPress={takePicture} style={styles.captureOuter}>
            <View style={styles.captureInner} />
          </TouchableOpacity>

          {/* Spacer to balance layout */}
          <View style={styles.spacer} />
        </View>
      </View>
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  cameraContainer: {
    flex: 1,
    position: "relative",
    borderRadius: 16,
    overflow: "hidden",
  },
  camera: {
    flex: 1,
  },

  /* Overlay */
  overlay: {
    position: "absolute",
    top: 24,
    alignSelf: "center",
    backgroundColor: "rgba(0,0,0,0.45)",
    paddingHorizontal: 18,
    paddingVertical: 6,
    borderRadius: 20,
  },
  overlayText: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "600",
  },

  /* Bottom Controls */
  bottomControls: {
    position: "absolute",
    bottom: 28,
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 32,
  },

  /* Gallery Button */
  galleryButton: {
    alignItems: "center",
    justifyContent: "center",
    marginRight: "auto",
  },
  galleryIcon: {
    fontSize: 28,
  },
  galleryLabel: {
    color: "#fff",
    fontSize: 11,
    marginTop: 2,
    fontWeight: "500",
  },

  /* Capture Button */
  captureOuter: {
    width: 72,
    height: 72,
    borderRadius: 36,
    borderWidth: 4,
    borderColor: "#FACC15",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(0,0,0,0.3)",
  },
  captureInner: {
    width: 54,
    height: 54,
    borderRadius: 27,
    backgroundColor: "#FACC15",
  },

  /* Spacer */
  spacer: {
    width: 56,
    marginLeft: "auto",
  },
});
