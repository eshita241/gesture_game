import cv2
import mediapipe as mp
import os
import time
import logging
import pyautogui
import platform

# Suppress TensorFlow Lite Warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open webcam properly with multiple attempts
def initialize_camera():
    for i in range(3):  # Try different camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            return cap
    return None

cap = initialize_camera()
if not cap:
    print("❌ ERROR: Cannot access the camera. Exiting.")
    exit()

print("✅ Camera initialized successfully!")

shutdown_flag = False  # Flag to track shutdown state
media_playing = True  # Assume media is playing for Spotify control
previous_index_x = None  # Store previous X coordinate of index finger tip
previous_middle_x = None  # Store previous X coordinate of middle finger tip

# Detect OS for correct keybinding
is_mac = platform.system() == "Darwin"
next_key = ["nexttrack"]
prev_key = ["prevtrack"]
left_arrow = ["left"]
right_arrow = ["right"]

# Hand Tracking Setup
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.8) as hands:
    
    while True:
        ret, frame = cap.read()
        
        # Attempt to reconnect if frame capture fails
        if not ret:
            print("❌ ERROR: Unable to capture frame. Retrying...")
            cap.release()
            time.sleep(2)
            cap = initialize_camera()
            if not cap:
                print("❌ ERROR: Camera unavailable after multiple attempts. Exiting.")
                break
            continue  # Skip this iteration and retry

        frame = cv2.flip(frame, 1)  # Mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hand detection
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get index and middle finger tip positions
                index_tip_x = hand_landmarks.landmark[8].x  # Index finger tip X coordinate
                middle_tip_x = hand_landmarks.landmark[12].x  # Middle finger tip X coordinate
                index_tip_y = hand_landmarks.landmark[8].y  # Index finger tip Y coordinate
                middle_tip_y = hand_landmarks.landmark[12].y  # Middle finger tip Y coordinate
                palm_y = hand_landmarks.landmark[0].y  # Palm Y coordinate for reference
                
                # Detect Two-Finger Swipe (Index and Middle Finger Overlapping)
                if abs(index_tip_x - middle_tip_x) < 0.3 and abs(index_tip_y - middle_tip_y) < 0.3:
                    if previous_index_x is not None and previous_middle_x is not None:
                        if index_tip_x - previous_index_x > 0.12 and middle_tip_x - previous_middle_x > 0.12:
                            print("➡️ TWO-FINGER SWIPE RIGHT DETECTED")
                            pyautogui.hotkey(*right_arrow)  # Right arrow key press
                        elif previous_index_x - index_tip_x > 0.12 and previous_middle_x - middle_tip_x > 0.12:
                            print("⬅️ TWO-FINGER SWIPE LEFT DETECTED")
                            pyautogui.hotkey(*left_arrow)  # Left arrow key press
                    previous_index_x = index_tip_x
                    previous_middle_x = middle_tip_x
                
                # Detect Single Finger Swipe (Avoid Interference with Two-Finger Swipes)
                elif media_playing and previous_index_x is not None:
                    if index_tip_x - previous_index_x > 0.12 and index_tip_y < palm_y - 0.05:
                        print("➡️ INDEX FINGER SWIPE RIGHT DETECTED - Next Song")
                        pyautogui.hotkey(*next_key)
                    elif previous_index_x - index_tip_x > 0.12 and index_tip_y < palm_y - 0.05:
                        print("⬅️ INDEX FINGER SWIPE LEFT DETECTED - Previous Song")
                        pyautogui.hotkey(*prev_key)
                previous_index_x = index_tip_x  # Store for next comparison

        # Display the webcam feed
        cv2.imshow("🖐 Hand Gesture OS Control", frame)

        # Exit on 'ESC' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()