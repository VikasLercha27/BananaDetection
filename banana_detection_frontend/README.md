# DoneWithIt (Expo React Native)

Mobile app to capture an image, send it to a backend for analysis, and show the prediction result.

## 1. Prerequisites

- Node.js 18+ (LTS recommended)
- npm 9+
- Git
- Expo Go app on your phone (Android/iOS) OR Android Studio / Xcode simulator
- Backend server running on port `3000`

## 2. Clone And Install

```bash
git clone <your-repo-url>
cd DoneWithIt
npm install
```

## 3. Start The App

```bash
npx expo start -c
```

Then:

- Press `a` for Android emulator, or
- Press `i` for iOS simulator, or
- Scan the QR in Expo Go.

## 4. Backend Requirements (Important)

The app sends:

- `POST /analyze`
- Request body: **raw image bytes** (not multipart form)
- `Content-Type`: `image/jpeg` or `image/png`

The backend should:

- listen on `0.0.0.0:3000`
- parse raw body for image types
- return prediction text or JSON

Example Express parser:

```js
app.use(
  "/analyze",
  express.raw({
    type: ["image/jpeg", "image/png", "application/octet-stream"],
    limit: "10mb",
  }),
);
```

## 5. API URL Behavior

Current app config is in `src/config/api.js`.

Resolution logic:

- Expo host LAN IP (best for phone + Expo Go)
- Android fallback: `http://10.0.2.2:3000`
- iOS fallback: `http://127.0.0.1:3000`
- Default fallback: `http://localhost:3000`
- Endpoint path default: `/analyze`

Optional override for endpoint path:

```powershell
$env:EXPO_PUBLIC_PREDICTION_PATH="/analyze"; npx expo start -c
```

## 6. Common Networking Setup (Expo Go On Phone)

- Phone and laptop must be on same Wi-Fi
- No guest network isolation
- VPN off on both devices
- Windows Firewall allows Node.js / port `3000`

If requests fail, test backend URL from phone browser:

- `http://<your-laptop-lan-ip>:3000/analyze`

## 7. Troubleshooting

### A) `Failed to download remote update`

This is Expo bundle delivery issue (not API code).

Try:

1. Stop all Expo/Metro processes.
2. Run: `npx expo start --tunnel -c`
3. Remove project from Expo Go recents and re-scan QR.
4. Disable VPN/proxy.
5. Ensure firewall allows Node.

### B) `Upload failed with status 404`

Backend route mismatch. Ensure server has `POST /analyze`.

### C) `Upload failed with status 400` and server says image body required

Server expects raw bytes. Ensure backend is using `express.raw(...)` and not multipart parsing for this route.

## 8. Project Scripts

From `package.json`:

- `npm run start` -> `expo start`
- `npm run android` -> `expo start --android`
- `npm run ios` -> `expo start --ios`
- `npm run web` -> `expo start --web`
