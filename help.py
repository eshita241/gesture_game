import cv2
import mediapipe as mp
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access camera.")
    exit()

# Initialize system volume control (Windows Only)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Initialize hand tracking
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    prev_wrist_y = None  # Store previous wrist Y-coordinate
    last_action_time = time.time()  # Prevent spamming volume changes

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip for mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hand detection
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get wrist Y-coordinate (landmark 0)
                wrist_y = hand_landmarks.landmark[0].y  # Normalized value (0-1)

                # Detect movement direction (Up or Down)
                if prev_wrist_y is not None:
                    if wrist_y < prev_wrist_y - 0.05:  # Hand moved UP
                        if time.time() - last_action_time > 0.5:  # Prevent spam
                            print("VOLUME UP")
                            try:
                                volume.SetMasterVolumeLevelScalar(min(1.0, volume.GetMasterVolumeLevelScalar() + 0.05), None)
                            except:
                                pyautogui.press("volumeup")
                            last_action_time = time.time()
                    
                    elif wrist_y > prev_wrist_y + 0.05:  # Hand moved DOWN
                        if time.time() - last_action_time > 0.5:
                            print("VOLUME DOWN")
                            try:
                                volume.SetMasterVolumeLevelScalar(max(0.0, volume.GetMasterVolumeLevelScalar() - 0.05), None)
                            except:
                                pyautogui.press("volumedown")
                            last_action_time = time.time()

                # Update previous wrist Y-coordinate
                prev_wrist_y = wrist_y

        # Display the webcam feed
        cv2.imshow("Hand Gesture Volume Control", frame)

        # Exit on 'ESC' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()
