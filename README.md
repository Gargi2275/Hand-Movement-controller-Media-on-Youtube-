# Hand Gesture Control (YouTube Media Controller)

This project controls **YouTube video playback** using **hand gestures** via your webcam.

It uses:
- **OpenCV** for webcam video capture
- **MediaPipe Tasks API** (`HandLandmarker`) for hand detection
- **pynput** to send keyboard shortcuts to YouTube

---

## Features

✅ Volume Up / Down  
✅ Play / Pause  
✅ Forward / Backward  
✅ Works with YouTube (Chrome/Edge/Firefox)

---

## Gesture Controls

| Gesture | Action | YouTube Key |
|--------|--------|-------------|
| Index finger above middle finger | Volume Up | ↑ (Up Arrow) |
| Index finger below middle finger | Volume Down | ↓ (Down Arrow) |
| Swipe hand to the right | Forward 5 seconds | `L` |
| Swipe hand to the left | Backward 5 seconds | `J` |
| Open Palm (all fingers up) | Play | `K` |
| Closed Fist (all fingers down) | Pause | `K` |

---

## Requirements

- Python **3.9 / 3.10 / 3.11** recommended
- Webcam (Laptop camera is fine)

---

## Installation

### 1) Create a Virtual Environment (Recommended)

Using conda:

```bash
conda create -n gesture_env python=3.10
conda activate gesture_env
```

### 2) Install Required Packages

```bash
pip install opencv-python mediapipe pynput
```

---

## Download the MediaPipe Model File

This project needs the model file:

📌 `hand_landmarker.task`

Download it from:

https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

Place it in the **same folder** as your Python script:


## Run the Project

```bash
python hand_gesture_control.py
```

Press **Q** to quit.

---

## Important Notes

### 1) Click on YouTube Video First
Make sure the YouTube video is focused (click on it once).  
Otherwise shortcuts won’t work.

### 2) Keep Cooldown Time
The code has a cooldown delay to prevent multiple triggers.

You can adjust it here:

```python
cooldown = 1.2
```

---

## Troubleshooting

### Media keys not working?
This project uses YouTube keyboard shortcuts, not system media keys.

### Webcam not opening?
Try changing camera index:

```python
cap = cv2.VideoCapture(1)
```

---

## Files Included

- `hand_gesture_control.py` → main program
- `hand_landmarker.task` → MediaPipe hand model (download separately)

---

## Author
Gargi Vanjara
Made for AI hand gesture media control project 🚀
