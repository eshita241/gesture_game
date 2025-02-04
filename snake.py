import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not working")
    exit()
else:
    print("Camera is working")

screen_width, screen_height = pyautogui.size()

min_x, max_x = 0, screen_width
min_y, max_y = 0, screen_height

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_tip = hand_landmarks.landmark[8]

                index_finger_x = int(index_finger_tip.x * screen_width)
                index_finger_y = int(index_finger_tip.y * screen_height)

                # Move cursor instantly to match finger movement
                pyautogui.moveTo(index_finger_x, index_finger_y, duration=0)

                cv2.putText(frame, "Cursor Control", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Index Finger Cursor Control', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
