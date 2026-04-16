// import { Platform } from "react-native";
// import Constants from "expo-constants";

// const EXPO_HOST_URI =
//   Constants.expoConfig?.hostUri || Constants.manifest?.debuggerHost || "";
// const EXPO_LAN_IP = EXPO_HOST_URI.split(":")[0] || "";

// const DEVICE_BASE_URL = EXPO_LAN_IP ? `http://${EXPO_LAN_IP}:5000` : "";

// const FALLBACK_BASE_URL = Platform.select({
//   android: "http://10.0.2.2:5000",
//   ios: "http://127.0.0.1:5000",
//   default: "http://localhost:5000",
// });

// export const API_BASE_URL = DEVICE_BASE_URL || FALLBACK_BASE_URL;

// const RAW_PREDICTION_PATH =
//   process.env.EXPO_PUBLIC_PREDICTION_PATH || "/predict";
// const NORMALIZED_PREDICTION_PATH = RAW_PREDICTION_PATH.startsWith("/")
//   ? RAW_PREDICTION_PATH
//   : `/${RAW_PREDICTION_PATH}`;

// export const PREDICTION_URL = `${API_BASE_URL}${NORMALIZED_PREDICTION_PATH}`;
import { Platform } from "react-native";
import Constants from "expo-constants";

// ── Auto-detect LAN IP from Expo dev server ──────────────────────
const EXPO_HOST_URI =
  Constants.expoConfig?.hostUri || Constants.manifest?.debuggerHost || "";
const EXPO_LAN_IP = EXPO_HOST_URI.split(":")[0] || "";

// ── FastAPI now runs on port 8000 (was 5000 with Flask) ──────────
const PORT = 8000;

const DEVICE_BASE_URL = EXPO_LAN_IP
  ? `http://${EXPO_LAN_IP}:${PORT}`
  : "";

const FALLBACK_BASE_URL = Platform.select({
  android: `http://10.0.2.2:${PORT}`,
  ios    : `http://127.0.0.1:${PORT}`,
  default: `http://localhost:${PORT}`,
});

export const API_BASE_URL = DEVICE_BASE_URL || FALLBACK_BASE_URL;

const RAW_PREDICTION_PATH =
  process.env.EXPO_PUBLIC_PREDICTION_PATH || "/predict";

const NORMALIZED_PREDICTION_PATH = RAW_PREDICTION_PATH.startsWith("/")
  ? RAW_PREDICTION_PATH
  : `/${RAW_PREDICTION_PATH}`;

export const PREDICTION_URL = `${API_BASE_URL}${NORMALIZED_PREDICTION_PATH}`;
export const HEALTH_URL     = `${API_BASE_URL}/health`;