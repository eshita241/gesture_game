import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Track which key is currently pressed
current_key = None

def release_key():
    """Releases the currently pressed key if any."""
    global current_key
    if current_key:
        pyautogui.keyUp(current_key)
        print(f"Released {current_key} key")
        current_key = None

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip frame horizontally to mirror user movement
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = hands.process(rgb_frame)

    detected_right_palm = False
    detected_left_palm = False

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'

            # Check if palm is open
            finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
            finger_mcp = [5, 9, 13, 17]  # MCP joints (base of fingers)
            is_open = all(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y for tip, mcp in zip(finger_tips, finger_mcp))

            if hand_label == "Right" and is_open:
                detected_right_palm = True
            elif hand_label == "Left" and is_open:
                detected_left_palm = True

    # Prioritize braking (left palm) over acceleration (right palm)
    if detected_left_palm:
        if current_key != 'left':
            release_key()  # Release previous key if switching
            pyautogui.keyDown('left')
            current_key = 'left'
            print("Braking - Left Arrow Key Down")

    elif detected_right_palm:
        if current_key != 'right':
            release_key()  # Release previous key if switching
            pyautogui.keyDown('right')
            current_key = 'right'
            print("Accelerating - Right Arrow Key Down")

    else:
        release_key()  # Release key when no hand is shown

    # Display frame
    cv2.imshow("Hill Climb Racing Hand Control", frame)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
