import { View, Text, Image, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function AppLayout({ children, title }) {
  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerText}>{"Ripen AI"}</Text>
        <Image source={require("../../assets/logo.png")} style={styles.logo} />
      </View>

      {/* Screen Content */}
      <View style={styles.content}>{children}</View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F1E8", // beige (global)
  },
  header: {
    height: 70,
    backgroundColor: "#FACC15", // mango yellow
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
  },
  headerText: {
    fontSize: 18,
    fontWeight: "600",
    color: "#1F2937",
  },
  logo: {
    width: 56,
    height: 56,
    resizeMode: "contain",
    borderRadius: 50,
  },
  content: {
    flex: 1,
    padding: 16,
  },
});
