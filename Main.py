import cv2
import mediapipe as mp
import time
import numpy as np
import pyttsx3

# --- INITIALIZATION ---
engine = pyttsx3.init()
engine.setProperty('rate', 160)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

MORSE_DICT = {
    '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F',
    '--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L',
    '--':'M','-.':'N','---':'O', '.--.':'P','--.-':'Q','.-.':'R',
    '...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
    '-.--':'Y','--..':'Z'
}

# Settings
DELAY_INTERVAL = 1.0 
last_action_time = 0
current_morse = ""
final_text = ""

def get_gesture_info(hand_landmarks):
    tip_ids = [8, 12, 16, 20]
    fingers_count = 0
    for tip in tip_ids:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_count += 1
    
    thumb_tip = hand_landmarks.landmark[4]
    thumb_base = hand_landmarks.landmark[3]
    thumb_open = abs(thumb_tip.x - hand_landmarks.landmark[0].x) > abs(thumb_base.x - hand_landmarks.landmark[0].x)
    return fingers_count, thumb_open

def draw_sidebar(img):
    h, w, _ = img.shape
    sidebar_w = 250
    sidebar = np.zeros((h, sidebar_w, 3), dtype=np.uint8) + 20
    cv2.putText(sidebar, "MORSE KEY", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    items = list(MORSE_DICT.items())
    mid = len(items) // 2
    y = 80
    for code, char in items[:mid]:
        cv2.putText(sidebar, f"{char}: {code}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        y += 25
    y = 80
    for code, char in items[mid:]:
        cv2.putText(sidebar, f"{char}: {code}", (130, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        y += 25
    return sidebar

# Initialize Window
cv2.namedWindow("Morse Conversation Mode", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Morse Conversation Mode", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    # Resize frame to fill height while keeping aspect ratio or stretching for full screen
    frame = cv2.resize(frame, (1280, 720)) 
    h, w, c = frame.shape
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    now = time.time()
    time_elapsed = now - last_action_time
    ready_for_input = time_elapsed > DELAY_INTERVAL

    if results.multi_hand_landmarks:
        hand_lms = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
        fingers, thumb_open = get_gesture_info(hand_lms)

        if fingers == 0 and not thumb_open and current_morse != "":
            if current_morse in MORSE_DICT:
                final_text += MORSE_DICT[current_morse]
            current_morse = ""
            last_action_time = now 

        elif ready_for_input:
            action_triggered = False
            if thumb_open and fingers == 0:
                final_text += " "
                action_triggered = True
            elif fingers == 1:
                current_morse += "."
                action_triggered = True
            elif fingers == 2:
                current_morse += "-"
                action_triggered = True
            elif fingers == 3:
                if final_text: final_text = final_text[:-1]
                action_triggered = True
            elif fingers == 4:
                if final_text:
                    engine.say(final_text)
                    engine.runAndWait()
                action_triggered = True
            elif fingers >= 5:
                current_morse = ""
                action_triggered = True
            
            if action_triggered:
                last_action_time = now

    # --- UI DESIGN FOR FULL SCREEN ---
    # Darken bottom area for text readability
    cv2.rectangle(frame, (0, h-150), (w, h), (0, 0, 0), -1)
    cv2.line(frame, (0, h-150), (w, h-150), (0, 255, 255), 2)

    # Display Morse Buffer
    cv2.putText(frame, f"INPUT: {current_morse}", (30, h-110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    # Display Sentence (with basic overflow check)
    display_text = final_text if len(final_text) < 50 else "..." + final_text[-47:]
    cv2.putText(frame, f"CONVERSATION: {display_text}", (30, h-50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Cooldown Bar
    remaining_wait = max(0, DELAY_INTERVAL - (now - last_action_time))
    bar_width = int((remaining_wait / DELAY_INTERVAL) * w)
    cv2.rectangle(frame, (0, h-10), (bar_width, h), (0, 255, 255), -1)

    # Combine Sidebar
    sidebar = draw_sidebar(frame)
    final_img = np.hstack((frame, sidebar))

    cv2.imshow("Morse Conversation Mode", final_img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()