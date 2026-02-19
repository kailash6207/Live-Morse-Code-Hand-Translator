# 🖐️ Live Morse Code Hand Translator

A Python-based real-time Morse code translator that uses **Computer Vision** to convert hand gestures into text and speech. Designed for full-screen use in video calls and conversations.

## ✨ Key Features
- **Real-time Detection:** High-speed hand tracking using MediaPipe.
- **Instant Locking:** 0-finger gesture locks letters immediately for faster communication.
- **Speech Synthesis:** 4-finger gesture reads the whole sentence out loud.
- **Full-Screen HUD:** Professional UI with a built-in Morse reference chart.

## 🎮 Gesture Controls
Gesture,Action
☝️ 1 Finger,Add a Dot (.)
✌️ 2 Fingers,Add a Dash (-)
✊ Fist (0 Fingers),Lock Letter (Instant)
🤟 3 Fingers,Backspace (Delete last letter)
🖖 4 Fingers,Speak (Read entire sentence)
👍 Thumb Only,Add Space
✋ 5 Fingers,Clear Morse Buffer

## 🚀 How to Run
1. **Install requirements:**
   `pip install opencv-python mediapipe numpy pyttsx3`
2. **Run the script:**
   `python main.py`
3. **Exit:** Press `Esc` or `q`.

---
**Developed by:** Kailash N H
