import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pynput.keyboard import Controller, Key
import time

# -------------------- Setup --------------------
keyboard = Controller()

# Make sure "hand_landmarker.task" is in your folder!
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# Swipe Tracking
swipe_start_pos = None
swipe_start_time = 0

last_action_time = 0
cooldown = 0.8  # Reduced slightly for better responsiveness
is_paused = False

# -------------------- Gesture Detection --------------------

def detect_gesture(landmarks, current_pos, width, height):
    global swipe_start_pos, swipe_start_time

    # Volume Logic (Index vs Middle height)
    index_y = landmarks[8].y * height
    middle_y = landmarks[12].y * height

    if index_y < middle_y - 45: return "volume_up"
    if index_y > middle_y + 45: return "volume_down"

    # Swipe Logic (Improved)
    curr_time = time.time()
    if swipe_start_pos is None:
        swipe_start_pos = current_pos
        swipe_start_time = curr_time
    
    # Check movement over a 0.2 second window
    if curr_time - swipe_start_time > 0.2:
        move_x = current_pos[0] - swipe_start_pos[0]
        swipe_start_pos = current_pos # Reset window
        swipe_start_time = curr_time

        if move_x > 50: return "forward"
        if move_x < -50: return "backward"

    # Open Palm vs Fist
    middle_mcp_y = landmarks[9].y
    fingers_y = [landmarks[i].y for i in [8, 12, 16, 20]]
    
    if all(y < middle_mcp_y for y in fingers_y): return "play"
    if all(y > middle_mcp_y for y in fingers_y): return "pause"

    return None

# -------------------- Main Loop --------------------

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for landmarks in result.hand_landmarks:
            # --- DRAW POINTS ON HAND ---
            for lm in landmarks:
                cx, cy = int(lm.x * width), int(lm.y * height)
                cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

            current_position = (int(landmarks[0].x * width), int(landmarks[0].y * height))
            gesture = detect_gesture(landmarks, current_position, width, height)
            current_time = time.time()

            if gesture and current_time - last_action_time > cooldown:
                if gesture == "volume_up":
                    keyboard.press(Key.up); keyboard.release(Key.up)
                    print("↑ Volume")
                elif gesture == "volume_down":
                    keyboard.press(Key.down); keyboard.release(Key.down)
                    print("↓ Volume")
                elif gesture == "forward":
                    keyboard.press('l'); keyboard.release('l')
                    print("→ Forward")
                elif gesture == "backward":
                    keyboard.press('j'); keyboard.release('j')
                    print("← Backward")
                elif gesture == "play" and is_paused:
                    keyboard.press('k'); keyboard.release('k')
                    is_paused = False; print("Play")
                elif gesture == "pause" and not is_paused:
                    keyboard.press('k'); keyboard.release('k')
                    is_paused = True; print("Pause")

                last_action_time = current_time

    cv2.imshow("Gesture Control (Q to Quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()