import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_action_time = 0

def detect_hand(handedness):
    global last_action_time

    if time.time() - last_action_time < 2:
        return

    if handedness == "Right": 
        pyautogui.press('right')
        print("Next Slide")
        last_action_time = time.time()

    elif handedness == "Left":  
        pyautogui.press('left')
        print("Previous Slide")
        last_action_time = time.time()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = hands.process(image_rgb)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            handedness_label = hand_handedness.classification[0].label
            detect_hand(handedness_label)

    cv2.imshow('Hand Gesture PPT Controller', image)

    if cv2.waitKey(5) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()