import cv2
import pyautogui
import time
import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ----------------------------
# Initialize webcam
# ----------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Cannot open webcam. Make sure it's connected and accessible.")

# ----------------------------
# Initialize MediaPipe HandLandmarker
# ----------------------------
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")  # we will download below
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.LIVE_STREAM,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

# Screen size
screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0
smoothening = 7
prev_time = 0

# ----------------------------
# Main loop
# ----------------------------
while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Run hand detection
    mp_image = vision.Image(image_format=vision.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect_for_video(mp_image, int(time.time() * 1000))

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            # Get landmark positions
            index = hand_landmarks[8]
            thumb = hand_landmarks[4]
            middle = hand_landmarks[12]

            ix, iy = int(index.x * w), int(index.y * h)
            tx, ty = int(thumb.x * w), int(thumb.y * h)
            mx, my = int(middle.x * w), int(middle.y * h)

            screen_x = int(ix * screen_w / w)
            screen_y = int(iy * screen_h / h)

            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            distance = math.hypot(tx - ix, ty - iy)
            distance2 = math.hypot(mx - ix, my - iy)

            # LEFT CLICK
            if distance < 0.04:  # normalized distance in 0..1
                pyautogui.click()
                time.sleep(0.3)
            # RIGHT CLICK
            elif distance2 < 0.04:
                pyautogui.rightClick()
                time.sleep(0.3)
            # SCROLL
            if ty < iy - 40:
                pyautogui.scroll(20)
            elif ty > iy + 40:
                pyautogui.scroll(-20)

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()