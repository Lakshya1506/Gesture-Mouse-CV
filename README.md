# 🖐️ HandControlledMouse

> Control your computer's mouse using just your hand and a webcam — no hardware required.

HandControlledMouse is a real-time, computer-vision-powered virtual mouse that maps your hand gestures to full mouse control: cursor movement, left click, right click, and scroll — all through a standard webcam feed.

---

## 📸 Demo

```
Index finger  →  Move cursor
Index + Thumb (pinch)  →  Left Click
Index + Middle (pinch)  →  Right Click
Thumb above/below Index  →  Scroll Up / Down
```

---

## ✨ Features

| Gesture | Action |
|---|---|
| Move index finger | Moves mouse cursor |
| Pinch index + thumb | Left click |
| Pinch index + middle | Right click |
| Thumb above index | Scroll up |
| Thumb below index | Scroll down |
| Press `Q` | Quit the application |

- **Smooth cursor movement** via exponential smoothing (no jitter)
- **Real-time FPS counter** displayed on the video feed
- **Single hand tracking** using MediaPipe's Hand Landmarker
- Works on any standard USB or built-in webcam

---

## 🛠️ Tech Stack

- **[OpenCV](https://opencv.org/)** — Webcam capture and display
- **[MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)** — Hand landmark detection
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** — System-level mouse and scroll control

---

## 📋 Requirements

- Python **3.8 – 3.11** (MediaPipe does not yet support Python 3.12+)
- A working **webcam**
- OS: **Windows**, **macOS**, or **Linux**

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/HandControlledMouse.git
cd HandControlledMouse
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe pyautogui
```

> **Linux users:** PyAutoGUI requires additional system packages:
> ```bash
> sudo apt-get install python3-tk python3-dev scrot
> ```

### 4. Download the MediaPipe Hand Landmarker model

Download `hand_landmarker.task` from the official MediaPipe release:

```bash
wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

Or manually download from:
**https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker**

Place the downloaded `hand_landmarker.task` file in the **same directory** as `HandControlledMouse.py`.

### 5. Verify your project structure

```
HandControlledMouse/
├── HandControlledMouse.py
├── hand_landmarker.task      ← must be here
└── README.md
```

---

## 🚀 Usage

```bash
python HandControlledMouse.py
```

A window titled **"AI Virtual Mouse"** will open showing your webcam feed.

| What you see | What it means |
|---|---|
| Green FPS counter (top-left) | App is running correctly |
| No hand landmarks shown | Hand not detected — try better lighting |
| Cursor not moving | Position your hand fully in frame |

**To exit:** Press `Q` while the webcam window is in focus.

---

## 🔧 Configuration

You can tune the following variables at the top of `HandControlledMouse.py`:

| Variable | Default | Description |
|---|---|---|
| `smoothening` | `7` | Higher = smoother but slower cursor movement |
| `distance` threshold | `0.04` | Pinch sensitivity for left click (normalized 0–1) |
| `distance2` threshold | `0.04` | Pinch sensitivity for right click (normalized 0–1) |
| `scroll` offset | `40px` | Pixel gap between thumb and index to trigger scroll |
| `num_hands` | `1` | Number of hands to track simultaneously |

---

## 🏗️ How It Works

```
Webcam Frame
     │
     ▼
Flip horizontally (mirror effect)
     │
     ▼
MediaPipe Hand Landmarker
     │  detects 21 landmarks per hand
     ▼
Extract key landmarks:
  • Index fingertip  (landmark 8)
  • Thumb tip        (landmark 4)
  • Middle fingertip (landmark 12)
     │
     ▼
Map index tip → screen coordinates
     │
     ▼
Apply exponential smoothing
     │
     ▼
PyAutoGUI moves/clicks/scrolls
```

The landmark coordinates from MediaPipe are normalized (0.0–1.0). They are multiplied by the screen dimensions to get absolute pixel positions. Smoothening is applied via a weighted interpolation between the previous and current position to eliminate jitter.

---

## ⚠️ Known Limitations

- **Click sensitivity** is distance-based only — accidental clicks may occur if fingers naturally rest close together. Consider adding a hold-duration threshold for production use.
- **Scroll behavior** fires continuously while the thumb position is held — it is not a one-shot trigger.
- **Screen boundary clamping** is not implemented; rapid hand movement near screen edges may cause PyAutoGUI warnings on some systems.
- **Lighting conditions** significantly affect detection accuracy. Use in a well-lit environment with a plain background for best results.

---

## 🗺️ Roadmap

- [ ] Add gesture for double-click
- [ ] Add drag-and-drop support
- [ ] Visual overlay for active gesture feedback
- [ ] Configurable sensitivity via CLI arguments
- [ ] Add hold-duration threshold to prevent accidental clicks
- [ ] Support for two-hand gestures

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [MediaPipe by Google](https://ai.google.dev/edge/mediapipe) for the hand landmark model
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for cross-platform mouse control
- [OpenCV](https://opencv.org/) for webcam and display utilities

---

<p align="center">Built with ❤️ using Python, OpenCV, and MediaPipe</p>
