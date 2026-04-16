# Banana Detection Frontend

This is the Expo React Native mobile frontend for the Banana Detection project. The app captures or selects a banana image, sends it to the backend for inference, and displays the prediction result.

## Features

* Expo-based React Native app
* Uses `expo-camera` and `expo-image-picker`
* Connects to the FastAPI backend prediction endpoint
* Supports Android, iOS, and web via Expo

## Prerequisites

* Node.js 18 or newer
* npm or yarn
* Expo CLI (optional, can use `npx expo`)
* Backend server running on port `8000`

## Installation

From the `banana_detection_frontend` directory:

```bash
npm install
```

or with yarn:

```bash
yarn install
```

## Running the App

Start the Expo development server:

```bash
npm start
```

Then choose one of these options:

* `npm run android` — launch Android emulator
* `npm run ios` — launch iOS simulator
* `npm run web` — open in browser
* Scan the QR code from Expo Go on a physical device

## Backend Connection

The frontend uses `src/config/api.js` to determine the backend URL.

By default, it expects the backend on port `8000`.

If you need a custom backend host/port, update `src/config/api.js` or configure Expo to use the correct LAN IP.

## API Endpoint

The frontend sends image uploads as multipart form data to:

```
POST /predict
```

Request fields:

* `image` — uploaded image file
* `model` — currently always `ann_classifier`

Example mobile payload is handled in `src/services/predictionService.js`.

## Project Structure

```text
banana_detection_frontend/
├── App.js
├── app.json
├── index.js
├── package.json
├── README.md
├── assets/
└── src/
    ├── components/
    │   └── AppLayout.js
    ├── config/
    │   └── api.js
    ├── navigation/
    │   └── AppNavigator.js
    ├── screens/
    │   ├── CameraScreen.js
    │   ├── HomeScreen.js
    │   ├── PreviewScreen.js
    │   └── ResultScreen.js
    └── services/
        └── predictionService.js
```

## Notes

* The current frontend is designed to work with the backend on `http://localhost:8000`.
* If using a physical device, make sure the phone and development machine are on the same network.
* Do not manually set the `Content-Type` header for multipart uploads in React Native; the app lets Expo handle it.

## Scripts

From `package.json`:

* `npm start` — start Expo dev server
* `npm run android` — open Android
* `npm run ios` — open iOS
* `npm run web` — open web browser

## Troubleshooting

* If the app can’t reach the backend, verify the backend is running and accessible on port `8000`.
* For Android emulator use `http://10.0.2.2:8000`.
* For iOS simulator use `http://127.0.0.1:8000`.

## License

This frontend is part of the Banana Detection project.
