import cv2
import mediapipe as mp
import numpy as np
import math
from pynput.keyboard import Key, Controller

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Previous midpoint for angle calculation
prev_midpoint = None

# Initialize keyboard controller
keyboard = Controller()

# Track key states
key_states = {
    'c': False, 'f': False, 'e': False, 'w': False, 'd': False,
    'left': False, 'right': False
}

def calculate_midpoint(hand_landmarks):
    x = (hand_landmarks.landmark[0].x + hand_landmarks.landmark[9].x) / 2
    y = (hand_landmarks.landmark[0].y + hand_landmarks.landmark[9].y) / 2
    return (int(x * frame.shape[1]), int(y * frame.shape[0]))

def calculate_angle(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    return math.degrees(math.atan2(y_diff, x_diff))

def get_direction(angle):
    if -45 <= angle <= 45:
        return "Right"
    elif 135 < angle or angle < -135:
        return "Left"
    else:
        return "Straight"

def detect_gestures(results):
    if not results.multi_hand_landmarks or len(results.multi_hand_landmarks) != 2:
        return None
    
    hand1 = results.multi_hand_landmarks[0]
    hand2 = results.multi_hand_landmarks[1]
    
    # Camera view change (C) - both index fingers extended
    if (hand1.landmark[8].y < hand1.landmark[5].y and 
        hand2.landmark[8].y < hand2.landmark[5].y):
        return 'c'
    
    # Nitro (F) - both little fingers extended
    elif (hand1.landmark[20].y < hand1.landmark[17].y and 
          hand2.landmark[20].y < hand2.landmark[17].y):
        return 'f'
    
    # Horn (E) - left hand palm open
    elif all(hand1.landmark[i].y < hand1.landmark[0].y for i in [8, 12, 16, 20]):
        return 'e'
    
    # Gear up (W) - palm facing up
    elif hand1.landmark[9].y > hand1.landmark[0].y:
        return 'w'
    
    # Gear down (D) - palm facing down
    elif hand1.landmark[9].y < hand1.landmark[0].y:
        return 'd'
    
    return None

def handle_key_press(key):
    if key in key_states:
        if not key_states[key]:
            keyboard.press(key)
            key_states[key] = True
            return f"Pressing {key.upper()}"
    return ""

def release_keys():
    for key in key_states:
        if key_states[key]:
            if key == 'left':
                keyboard.release(Key.left)
            elif key == 'right':
                keyboard.release(Key.right)
            else:
                keyboard.release(key)
            key_states[key] = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if not results.multi_hand_landmarks:
        release_keys()
    else:
        # Handle special gestures
        detected_key = detect_gestures(results)
        action_text = ""
        if detected_key:
            action_text = handle_key_press(detected_key)
            if action_text:
                cv2.putText(frame, action_text, (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Handle steering if two hands are detected
        if len(results.multi_hand_landmarks) == 2:
            midpoints = [calculate_midpoint(hand_landmarks) for hand_landmarks in results.multi_hand_landmarks]
            current_midpoint = ((midpoints[0][0] + midpoints[1][0]) // 2, (midpoints[0][1] + midpoints[1][1]) // 2)

            cv2.line(frame, midpoints[0], midpoints[1], (0, 255, 0), 2)
            cv2.circle(frame, current_midpoint, 5, (0, 0, 255), -1)

            if prev_midpoint:
                cv2.line(frame, prev_midpoint, current_midpoint, (255, 0, 0), 2)
                angle = calculate_angle(prev_midpoint, current_midpoint)
                direction = get_direction(angle)
                
                # Handle steering controls
                if direction == "Right":
                    keyboard.press(Key.right)
                    key_states['right'] = True
                elif direction == "Left":
                    keyboard.press(Key.left)
                    key_states['left'] = True
                else:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)
                    key_states['left'] = False
                    key_states['right'] = False

                cv2.putText(frame, f"Angle: {angle:.2f}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Direction: {direction}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            prev_midpoint = current_midpoint

        # Draw hand landmarks
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display active keys
    active_keys = [k.upper() for k, v in key_states.items() if v]
    if active_keys:
        cv2.putText(frame, f"Active: {', '.join(active_keys)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Game Controls', frame)

    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

release_keys()
cap.release()
cv2.destroyAllWindows()