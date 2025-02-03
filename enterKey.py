import cv2
import mediapipe as mp
import pyautogui
import os  # ✅ Make sure this is imported

# Initialize MediaPipe and Webcam
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Helper function to detect thumb and pinky extended gesture
def is_thumb_pinky_up(landmarks):
    # Tip and PIP (proximal interphalangeal) joints for comparison
    fingers = {
        "index": (8, 6),
        "middle": (12, 10),
        "ring": (16, 14),
        "pinky": (20, 18),
        "thumb": (4, 2)
    }

    # Check if thumb and pinky are extended, other fingers are folded
    return (
        landmarks[fingers["thumb"][0]].y < landmarks[fingers["thumb"][1]].y and  # Thumb is up
        landmarks[fingers["pinky"][0]].y < landmarks[fingers["pinky"][1]].y and  # Pinky is up
        landmarks[fingers["index"][0]].y > landmarks[fingers["index"][1]].y and  # Index is folded
        landmarks[fingers["middle"][0]].y > landmarks[fingers["middle"][1]].y and  # Middle is folded
        landmarks[fingers["ring"][0]].y > landmarks[fingers["ring"][1]].y  # Ring is folded
    )

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Gesture: Thumb and Pinky Extended (Simulate Enter key)
                if is_thumb_pinky_up(hand_landmarks.landmark):
                    print("Thumb and Pinky Detected - Simulating Enter Key")
                    pyautogui.press('enter')

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
