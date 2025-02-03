import cv2
import mediapipe as mp
from pynput.keyboard import Controller
import time

# Initialize MediaPipe Hands and Keyboard Controller
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
keyboard = Controller()

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not working")
else:
    print("Camera is working")

def release_all_movement_keys():
    for key in ['w', 'a', 's', 'd', 'o']:
        keyboard.release(key)

# Track the last gesture and key pressed
last_gesture = None
current_key_pressed = None

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for natural interaction
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gesture = ""  # Current gesture
        key_to_press = ""  # Key to simulate

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get landmark coordinates
                landmarks = hand_landmarks.landmark
                wrist = landmarks[0]
                index_finger_tip = landmarks[8]
                index_finger_end = landmarks[5]
                middle_finger_tip = landmarks[12]
                middle_finger_end = landmarks[9]
                thumb_tip = hand_landmarks.landmark[4]
                thumb_base = hand_landmarks.landmark[2]

                dx_index = index_finger_tip.x - index_finger_end.x
                dy_index = index_finger_tip.y - index_finger_end.y
                dx_middle = middle_finger_tip.x - middle_finger_end.x
                dy_middle = middle_finger_tip.y - middle_finger_end.y

                fingertip_distances = [abs(hand_landmarks.landmark[i].y - hand_landmarks.landmark[0].y) for i in [8, 12, 16, 20]]
                fist_closed = all(dist < 0.05 for dist in fingertip_distances) and abs(thumb_tip.x - hand_landmarks.landmark[0].x) < 0.05
                fingers_folded = all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y for i in [8, 12, 16, 20])
                thumbs_up = thumb_tip.y < thumb_base.y and fingers_folded

                # Average the vectors to get combined direction
                dx = (dx_index + dx_middle) / 2
                dy = (dy_index + dy_middle) / 2

                if fist_closed:
                    gesture = "Stop"
                    key_to_press = ""
                elif thumbs_up:
                    gesture = "Shoot"
                    key_to_press = 'o'
                elif abs(dx) > abs(dy):
                    if dx > 0.1:
                        gesture = "Right"
                        key_to_press = 'd'
                    elif dx < -0.1:
                        gesture = "Left"
                        key_to_press = 'a'
                else:
                    if dy < -0.1:
                        gesture = "Up"
                        key_to_press = 'w'
                    elif dy > 0.1:
                        gesture = "Down"
                        key_to_press = 's'

                # Handle continuous key pressing
                if gesture != last_gesture:
                    if current_key_pressed:
                        keyboard.release(current_key_pressed)
                    if key_to_press:
                        keyboard.press(key_to_press)
                        current_key_pressed = key_to_press
                    else:
                        current_key_pressed = None

                    last_gesture = gesture

                # Display the gesture and key pressed
                cv2.putText(frame, f"Gesture: {gesture} | Key: {key_to_press if gesture else 'None'}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if current_key_pressed:
                keyboard.release(current_key_pressed)
                current_key_pressed = None
            last_gesture = None  # Reset when no hand detected

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

cap.release()
cv2.destroyAllWindows()
