<<<<<<< HEAD
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import AppLayout from '../components/AppLayout';
import * as ImagePicker from "expo-image-picker";
=======
import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import AppLayout from "../components/AppLayout";

>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
export default function HomeScreen({ navigation }) {
    const openGallery = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {
      alert("Permission to access gallery is required");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
    });

    if (!result.canceled) {
      navigation.navigate("Preview", {
        imageUri: result.assets[0].uri,
      });
    }
  };
  return (
    <AppLayout title="">
<<<<<<< HEAD

=======
      {/* Main Content */}
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
      <View style={styles.content}>

        {/* Mango Illustration */}
        <Image
          source={require('../../assets/logo.png')}
          style={styles.image}
        />

        <Text style={styles.title}>Organic Ripeness Detector</Text>

        <Text style={styles.subtitle}>
<<<<<<< HEAD
          Scan bananas to detect artificial ripening using AI
=======
          Scan banana to detect artificial ripening using AI
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
        </Text>

        {/* Camera Button */}
        <TouchableOpacity
<<<<<<< HEAD
          style={styles.cameraButton}
          onPress={() => navigation.navigate('Camera')}
=======
          style={styles.button}
          onPress={() => navigation.navigate("Camera")}
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
        >
          <Text style={styles.buttonText}>📷 Scan with Camera</Text>
        </TouchableOpacity>

        {/* Gallery Button */}
        <TouchableOpacity
          style={styles.galleryButton}
          onPress={openGallery}
        >
          <Text style={styles.buttonText}>🖼 Upload from Gallery</Text>
        </TouchableOpacity>

      </View>
    </AppLayout>
  );
}

const styles = StyleSheet.create({

  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 24,
  },

  image: {
    width: 180,
    height: 180,
    resizeMode: 'contain',
    marginBottom: 20,
  },

  title: {
    fontSize: 26,
    fontWeight: "700",
    color: "#1F2937",
    textAlign: "center",
    marginBottom: 8,
  },

  subtitle: {
    fontSize: 15,
<<<<<<< HEAD
    color: '#4B5563',
    textAlign: 'center',
    marginBottom: 30,
  },

  cameraButton: {
    width: '80%',
    backgroundColor: '#FACC15',
=======
    color: "#4B5563",
    textAlign: "center",
    marginBottom: 32,
  },

  /* Button */
  button: {
    backgroundColor: "#FACC15", // professional green
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },

  galleryButton: {
    width: '80%',
    backgroundColor: '#16A34A',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },

  buttonText: {
<<<<<<< HEAD
    color: '#000',
=======
    color: "#000000",
>>>>>>> ca2ef8ef689f09e42d394501fee03249ceb0a924
    fontSize: 16,
    fontWeight: "600",
  },

});