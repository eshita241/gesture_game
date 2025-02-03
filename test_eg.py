import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open the webcam
cap = cv2.VideoCapture(0)  # Change to 1 if 0 doesn't work

gesture_mapping = {}

def define_gesture():
    """Function to define a new gesture and map it to a key."""
    gesture_name = input("Enter gesture name: ")
    mapped_key = input("Enter key to map this gesture (e.g., 'q', 'e', 'space'): ")

    print("Make the gesture and hold it for 3 seconds...")

    start_time = time.time()
    recorded_landmarks = None

    while time.time() - start_time < 3:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                recorded_landmarks = [
                    (lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark
                ]
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Camera", frame)
        cv2.waitKey(1)

    if recorded_landmarks:
        gesture_mapping[gesture_name] = (mapped_key, recorded_landmarks)
        print(f"Gesture '{gesture_name}' mapped to key '{mapped_key}'!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Press 'q' to quit
        break
    elif key == ord("d"):  # Press 'd' to define a new gesture
        define_gesture()

cap.release()
cv2.destroyAllWindows()
