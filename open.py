import cv2
import mediapipe as mp
import pyautogui
import subprocess

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Function to launch applications
def launch_app(app_name):
    apps = {
        "figma": r"C:/Users/harsh/AppData/Local/Figma/Figma.exe"
    }
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        print(f"Launching {app_name}...")
    else:
        print("App not found!")

# Capture Webcam Feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert Frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extracting Finger Tip Landmarks
            index_finger_tip = hand_landmarks.landmark[8]  # Index Finger Tip
            thumb_tip = hand_landmarks.landmark[4]  # Thumb Tip
            pinky_tip = hand_landmarks.landmark[20]  # Pinky Tip

            # Gesture 1: Thumbs Up → Open Spotify
            if thumb_tip.y < index_finger_tip.y and thumb_tip.y < pinky_tip.y:
                launch_app("figma")

    # Show Video Feed
    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
