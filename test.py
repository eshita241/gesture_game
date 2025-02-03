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

# Function to simulate key press and release
def press_key(key):
    keyboard.press(key)
    time.sleep(0.1)  # Short delay to simulate real key press
    keyboard.release(key)

# Track the last gesture to prevent repeated key presses
last_gesture = None

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

                dx_index = index_finger_tip.x - index_finger_end.x
                dy_index = index_finger_tip.y - index_finger_end.y

                dx_middle = middle_finger_tip.x - middle_finger_end.x
                dy_middle = middle_finger_tip.y - middle_finger_end.y

                # Average the vectors to get combined direction
                dx = (dx_index + dx_middle) / 2
                dy = (dy_index + dy_middle) / 2

                # Determine gesture based on movement
                if abs(dx) > abs(dy):
                    if dx > 0.05:
                        gesture = "Right"
                        key_to_press = 'd'
                    elif dx < -0.05:
                        gesture = "Left"
                        key_to_press = 'a'
                else:
                    if dy < -0.05:
                        gesture = "Up"
                        key_to_press = 'w'
                    elif dy > 0.05:
                        gesture = "Down"
                        key_to_press = 's'

                # Only trigger key press if the gesture has changed
                if gesture != "" and gesture != last_gesture:
                    press_key(key_to_press)
                    last_gesture = gesture

                # Display the gesture and key pressed
                cv2.putText(frame, f"Gesture: {gesture} | Key: {key_to_press if gesture else 'None'}",
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        else:
            last_gesture = None  # Reset when no hand detected

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

cap.release()
cv2.destroyAllWindows()
