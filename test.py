import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not working")
else:
    print("Camera is working")


# Function to calculate angle between three points
def calculate_angle(a, b, c):
    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    )
    return abs(angle)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for natural interaction
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get landmark coordinates
                landmarks = hand_landmarks.landmark
                x_list = [lm.x for lm in landmarks]
                y_list = [lm.y for lm in landmarks]

                # Determine the direction of the gesture
                wrist = landmarks[0]
                index_finger_tip = landmarks[8]

                dx = index_finger_tip.x - wrist.x
                dy = index_finger_tip.y - wrist.y

                gesture = ""
                if abs(dx) > abs(dy):
                    if dx > 0.1:
                        gesture = "Right"
                    elif dx < -0.1:
                        gesture = "Left"
                else:
                    if dy < -0.1:
                        gesture = "Up"
                    elif dy > 0.1:
                        gesture = "Down"

                # Display the gesture
                cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

cap.release()
cv2.destroyAllWindows()
