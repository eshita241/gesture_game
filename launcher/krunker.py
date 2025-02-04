import cv2
import mediapipe as mp
from pynput.keyboard import Controller
from pynput.mouse import Controller as MouseController, Button
import time
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
keyboard = Controller()
mouse = MouseController()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not working")
else:
    print("Camera is working")

def release_all_movement_keys():
    for key in ['w', 'a', 's', 'd', '\\']:
        keyboard.release(key)

last_gesture = None
current_key_pressed = None

screen_width, screen_height = 1920, 1080

min_x, max_x = 100, screen_width - 100
min_y, max_y = 100, screen_height - 100

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gesture = ""
        key_to_press = ""

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark
                wrist = landmarks[0]
                index_finger_tip = landmarks[8]
                index_finger_end = landmarks[5]
                middle_finger_tip = landmarks[12]
                middle_finger_end = landmarks[9]
                thumb_tip = landmarks[4]
                thumb_base = landmarks[2]

                fist_threshold = 0.08  
                fingertip_distances = [abs(landmarks[i].y - landmarks[0].y) for i in [8, 12, 16, 20]]
                fist_closed = all(dist < fist_threshold for dist in fingertip_distances) and abs(thumb_tip.x - landmarks[0].x) < fist_threshold

                fingers_folded = all(landmarks[i].y > landmarks[i - 2].y + 0.03 for i in [8, 12, 16, 20])

                thumbs_up = thumb_tip.y < thumb_base.y and fingers_folded

                dx_index = index_finger_tip.x - index_finger_end.x
                dy_index = index_finger_tip.y - index_finger_end.y
                dx_middle = middle_finger_tip.x - middle_finger_end.x
                dy_middle = middle_finger_tip.y - middle_finger_end.y

                dx_threshold = 0.07  
                dy_threshold = 0.07

                dx = (dx_index + dx_middle) / 2
                dy = (dy_index + dy_middle) / 2

                if fist_closed:
                    gesture = "Stop"
                    key_to_press = ""
                elif thumbs_up:
                    gesture = "Shoot"
                    key_to_press = '\\'
                elif abs(dx) > abs(dy):
                    if dx > dx_threshold:
                        gesture = "Right"
                        key_to_press = 'd'
                    elif dx < -dx_threshold:
                        gesture = "Left"
                        key_to_press = 'a'
                else:
                    if dy < -dy_threshold:
                        gesture = "Up"
                        key_to_press = 'w'
                    elif dy > dy_threshold:
                        gesture = "Down"
                        key_to_press = 's'

                if gesture != last_gesture:
                    if current_key_pressed:
                        keyboard.release(current_key_pressed)
                    if key_to_press:
                        keyboard.press(key_to_press)
                        current_key_pressed = key_to_press
                    else:
                        current_key_pressed = None

                    last_gesture = gesture

                index_finger_x = int(index_finger_tip.x * screen_width)
                index_finger_y = int(index_finger_tip.y * screen_height)

                index_finger_x = max(min_x, min(index_finger_x, max_x))
                index_finger_y = max(min_y, min(index_finger_y, max_y))

                mouse.position = (index_finger_x, index_finger_y)

                thumb_index_click_threshold = 0.08
                thumb_index_dist = abs(thumb_tip.x - index_finger_tip.x) + abs(thumb_tip.y - index_finger_tip.y)
                if thumb_index_dist < thumb_index_click_threshold:
                    gesture = "Click"
                    print("Click Detected!")
                    mouse.click(Button.left)
                    pyautogui.click(x=index_finger_x, y=index_finger_y)

                cv2.putText(frame, f"Gesture: {gesture} | Key: {key_to_press if gesture else 'None'}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if current_key_pressed:
                keyboard.release(current_key_pressed)
                current_key_pressed = None
            last_gesture = None

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
