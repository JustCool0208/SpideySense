import cv2
import threading
import time
import queue
from collections import Counter

from object_detector.yolo_detector import model
from object_detector.distance_estimator import estimate_distance
from voice_agent.stt_whisper import transcribe
from voice_agent.ai_brain import chat_with_gemini

import pyttsx3

# === TTS Safe Speak ===
speak_queue = queue.Queue()

def speak_worker():
    while True:
        msg = speak_queue.get()
        if msg:
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
            speak_queue.task_done()

threading.Thread(target=speak_worker, daemon=True).start()

def speak_async(text):
    speak_queue.put(text)

# === Globals ===
cap = cv2.VideoCapture(0)
dismissed = set()
last_spoken = {}
focal_length = 615
COOLDOWN = 10
latest_detected = []

KNOWN_WIDTHS = {
    "person": 50,
    "car": 180,
    "bicycle": 60
}

# === Helpers ===
def summarize_vision_context():
    if not latest_detected:
        return "nothing"
    counts = Counter(latest_detected)
    summary = ", ".join([f"{v} {k}{'s' if v > 1 else ''}" for k, v in counts.items()])
    return summary

def dismiss_temporarily(name, seconds=10):
    dismissed.add(name)
    print(f"[Dismissed] {name} for {seconds}s")
    threading.Timer(seconds, lambda: dismissed.discard(name)).start()

def handle_voice_command():
    speak_async("Voice command activated. You can speak now.")
    text = transcribe().lower()
    print(f"🗣️ You said: {text}")

    for obj in KNOWN_WIDTHS:
        if f"dismiss {obj}" in text:
            dismiss_temporarily(obj)
            speak_async(f"Okay, {obj} dismissed for now.")
            return

    object_summary = summarize_vision_context()
    prompt = f"You are my AI assistant connected to my smart camera.\n"
    prompt += f"Currently, I can see: {object_summary}.\n"
    prompt += f"Reply concisely in one short sentence to: {text}"

    reply = chat_with_gemini(prompt)
    print(f"🤖 Gemini: {reply}")
    speak_async(reply)

# === Main Loop ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)  # suppress logs
    latest_detected.clear()

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = r.names[cls]
            latest_detected.append(name)

            if name in KNOWN_WIDTHS:
                box_width = int(box.xywh[0][2])
                distance = estimate_distance(KNOWN_WIDTHS[name], focal_length, box_width)
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                label = f"{name} - {int(distance)} cm"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                now = time.time()
                if distance < 200 and name not in dismissed:
                    if name not in last_spoken or now - last_spoken[name] > COOLDOWN:
                        speak_async(f"Warning: {name} at {int(distance)} centimeters")
                        last_spoken[name] = now

    cv2.imshow("🕷️ SpideySense - AI Mode", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        print("🛑 Exiting SpideySense")
        break
    elif key == ord('d') and latest_detected:
        dismiss_temporarily(latest_detected[0])
    elif key == ord('v'):
        threading.Thread(target=handle_voice_command, daemon=True).start()
    elif key == ord('t'):
        user_input = input("📝 Type your command: ")
        object_summary = summarize_vision_context()
        prompt = f"You are my AI assistant connected to my smart camera for my safety.You are named SpideySense.\n"
        prompt += f"Currently, I can see: {object_summary} . This is the live feed extracted information.\n"
        prompt+=f"Your role is to alert me about the safety and also act as my personal assistant ready to assist"
        prompt += f"Reply concisely in one short sentence to: {user_input}"
        reply = chat_with_gemini(prompt)
        print(f"🤖 Gemini: {reply}")
        speak_async(reply)

cap.release()
cv2.destroyAllWindows()
