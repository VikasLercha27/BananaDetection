// import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
// import { SafeAreaView } from "react-native-safe-area-context";
// import AppLayout from "../components/AppLayout";

// export default function ResultScreen({ navigation, route }) {

//   const result = route?.params?.prediction;

//   const label = result?.label || "Unknown";
//   const confidence = result?.confidence
//     ? (result.confidence * 100).toFixed(2)
//     : null;
//   const model = result?.model || "N/A";

//   const isNatural = label.toLowerCase() === "natural";

//   return (
//     <AppLayout title="">
//       <SafeAreaView style={styles.container}>

//         <View style={styles.card}>

//           <Text style={styles.title}>Detection Result</Text>

//           <Text
//             style={[
//               styles.resultLabel,
//               isNatural ? styles.natural : styles.artificial,
//             ]}
//           >
//             {label.toUpperCase()}
//           </Text>

//           {confidence && (
//             <Text style={styles.confidence}>
//               Confidence: {confidence}%
//             </Text>
//           )}

//           <Text style={styles.model}>
//             Model Used: {model}
//           </Text>

//         </View>

//         <TouchableOpacity
//           style={styles.homeButton}
//           onPress={() => navigation.navigate("Home")}
//         >
//           <Text style={styles.homeButtonText}>Scan Another Mango</Text>
//         </TouchableOpacity>

//       </SafeAreaView>
//     </AppLayout>
//   );
// }

// const styles = StyleSheet.create({

//   container: {
//     flex: 1,
//     backgroundColor: "#F5F1E8",
//     justifyContent: "center",
//     alignItems: "center",
//     padding: 20,
//   },

//   card: {
//     width: "100%",
//     backgroundColor: "#FFFFFF",
//     borderRadius: 18,
//     padding: 30,
//     alignItems: "center",
//     elevation: 4,
//   },

//   title: {
//     fontSize: 20,
//     fontWeight: "600",
//     marginBottom: 20,
//     color: "#374151",
//   },

//   resultLabel: {
//     fontSize: 32,
//     fontWeight: "700",
//     marginBottom: 12,
//   },

//   natural: {
//     color: "#16A34A",
//   },

//   artificial: {
//     color: "#DC2626",
//   },

//   confidence: {
//     fontSize: 18,
//     color: "#4B5563",
//     marginBottom: 8,
//   },

//   model: {
//     fontSize: 16,
//     color: "#6B7280",
//   },

//   homeButton: {
//     marginTop: 30,
//     backgroundColor: "#FACC15",
//     paddingVertical: 16,
//     paddingHorizontal: 30,
//     borderRadius: 14,
//   },

//   homeButtonText: {
//     fontSize: 16,
//     fontWeight: "600",
//     color: "#1F2937",
//   },
// });
import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import AppLayout from "../components/AppLayout";

export default function ResultScreen({ navigation, route }) {

  const { prediction, imageUri } = route.params || {};

  const label      = prediction?.label      || "Unknown";
  const confidence = prediction?.confidence ?? null;
  const rawProb    = prediction?.raw_prob   ?? null;

  const isNatural    = label.toLowerCase() === "natural";
  const isArtificial = label.toLowerCase() === "artificial";

  const confPercent = confidence !== null
    ? (confidence * 100).toFixed(1)
    : null;

  // Confidence bar colour
  const barColor = confidence >= 0.95
    ? "#16A34A"
    : confidence >= 0.80
    ? "#F59E0B"
    : "#DC2626";

  return (
    <AppLayout title="">
      <SafeAreaView style={styles.container}>

        {/* Image thumbnail */}
        {imageUri && (
          <Image source={{ uri: imageUri }} style={styles.thumbnail} />
        )}

        {/* Result card */}
        <View style={styles.card}>

          <Text style={styles.title}>Detection Result</Text>

          {/* Label pill */}
          <View style={[
            styles.labelPill,
            isNatural    ? styles.pillNatural    :
            isArtificial ? styles.pillArtificial :
                           styles.pillUnknown
          ]}>
            <Text style={styles.labelPillText}>
              {isNatural ? "🌿" : isArtificial ? "⚠️" : "❓"}
              {"  "}
              {label.toUpperCase()}
            </Text>
          </View>

          {/* Description */}
          <Text style={styles.description}>
            {isNatural
              ? "This mango appears to be naturally ripened."
              : isArtificial
              ? "This mango may have been artificially ripened."
              : "Classification result unavailable."}
          </Text>

          {/* Confidence bar */}
          {confPercent !== null && (
            <View style={styles.confSection}>
              <View style={styles.confHeader}>
                <Text style={styles.confLabel}>Confidence</Text>
                <Text style={[styles.confValue, { color: barColor }]}>
                  {confPercent}%
                </Text>
              </View>
              <View style={styles.barTrack}>
                <View style={[
                  styles.barFill,
                  { width: `${confPercent}%`, backgroundColor: barColor }
                ]} />
              </View>
            </View>
          )}

          {/* Meta info */}
          <View style={styles.metaRow}>
            <View style={styles.metaChip}>
              <Text style={styles.metaChipText}>⚡ EfficientNetB0</Text>
            </View>
            <View style={styles.metaChip}>
              <Text style={styles.metaChipText}>🧠 ANN Classifier</Text>
            </View>
          </View>

        </View>

        {/* Scan another button */}
        <TouchableOpacity
          style={styles.homeButton}
          onPress={() => navigation.navigate("Home")}
        >
          <Text style={styles.homeButtonText}>  Scan Another Banana</Text>
        </TouchableOpacity>

        {/* Scan again with same image */}
        <TouchableOpacity
          style={styles.retryButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.retryButtonText}>← Try Different Image</Text>
        </TouchableOpacity>

      </SafeAreaView>
    </AppLayout>
  );
}

const styles = StyleSheet.create({
  container: {
    flex           : 1,
    backgroundColor: "#F5F1E8",
    padding        : 20,
    alignItems     : "center",
  },

  thumbnail: {
    width       : 120,
    height      : 120,
    borderRadius: 16,
    resizeMode  : "cover",
    marginBottom: 16,
    borderWidth : 3,
    borderColor : "#FACC15",
  },

  card: {
    width          : "100%",
    backgroundColor: "#FFFFFF",
    borderRadius   : 20,
    padding        : 24,
    alignItems     : "center",
    elevation      : 4,
    shadowColor    : "#000",
    shadowOpacity  : 0.08,
    shadowRadius   : 12,
    shadowOffset   : { width: 0, height: 4 },
  },

  title: {
    fontSize    : 16,
    fontWeight  : "600",
    color       : "#6B7280",
    marginBottom: 16,
    letterSpacing: 0.5,
    textTransform: "uppercase",
  },

  labelPill: {
    paddingHorizontal: 24,
    paddingVertical  : 12,
    borderRadius     : 50,
    marginBottom     : 14,
  },

  pillNatural: {
    backgroundColor: "#DCFCE7",
  },

  pillArtificial: {
    backgroundColor: "#FEE2E2",
  },

  pillUnknown: {
    backgroundColor: "#F3F4F6",
  },

  labelPillText: {
    fontSize  : 22,
    fontWeight: "800",
    color     : "#1F2937",
  },

  description: {
    fontSize   : 14,
    color      : "#6B7280",
    textAlign  : "center",
    marginBottom: 20,
    lineHeight : 20,
  },

  confSection: {
    width        : "100%",
    marginBottom : 20,
  },

  confHeader: {
    flexDirection : "row",
    justifyContent: "space-between",
    marginBottom  : 6,
  },

  confLabel: {
    fontSize  : 13,
    color     : "#6B7280",
    fontWeight: "500",
  },

  confValue: {
    fontSize  : 13,
    fontWeight: "700",
  },

  barTrack: {
    width          : "100%",
    height         : 10,
    backgroundColor: "#F3F4F6",
    borderRadius   : 10,
    overflow       : "hidden",
  },

  barFill: {
    height      : "100%",
    borderRadius: 10,
  },

  metaRow: {
    flexDirection: "row",
    gap          : 8,
  },

  metaChip: {
    backgroundColor : "#F9FAFB",
    paddingHorizontal: 12,
    paddingVertical  : 6,
    borderRadius     : 20,
    borderWidth      : 1,
    borderColor      : "#E5E7EB",
  },

  metaChipText: {
    fontSize : 11,
    color    : "#374151",
    fontWeight: "500",
  },

  homeButton: {
    marginTop      : 24,
    width          : "100%",
    backgroundColor: "#FACC15",
    paddingVertical: 16,
    borderRadius   : 14,
    alignItems     : "center",
  },

  homeButtonText: {
    fontSize  : 16,
    fontWeight: "700",
    color     : "#1F2937",
  },

  retryButton: {
    marginTop: 10,
    padding  : 12,
  },

  retryButtonText: {
    fontSize : 14,
    color    : "#6B7280",
    fontWeight: "500",
  },
});