import cv2
import threading
import time

from object_detector.yolo_detector import model
from object_detector.distance_estimator import estimate_distance
from voice_agent.tts_robotic import speak
from voice_agent.stt_whisper import transcribe
from voice_agent.ai_brain import chat_with_gemini

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
from collections import Counter

def summarize_vision_context():
    if not latest_detected:
        return "nothing"
    counts = Counter(latest_detected)
    summary = ", ".join([f"{v} {k}{'s' if v > 1 else ''}" for k, v in counts.items()])
    return summary


def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

def dismiss_temporarily(name, seconds=10):
    dismissed.add(name)
    print(f"[Dismissed] {name} for {seconds}s")
    threading.Timer(seconds, lambda: dismissed.discard(name)).start()

def handle_voice_command():
    text = transcribe().lower()
    print(f"🗣️ You said: {text}")

    # Voice Dismiss Logic
    for obj in KNOWN_WIDTHS:
        if f"dismiss {obj}" in text:
            dismiss_temporarily(obj)
            speak_async(f"Okay, {obj} dismissed for now.")
            return

    # 🔍 Add live vision context
    object_summary = summarize_vision_context()
    prompt = f"You are my AI assistant connected to my smart camera.\n"
    prompt += f"Currently, I can see: {object_summary}.\n"
    prompt += f"My question is: {text}"

    reply = chat_with_gemini(prompt)
    print(f"🤖 Gemini: {reply}")
    speak_async(reply)


    # Voice Dismiss Logic
    for obj in KNOWN_WIDTHS:
        if f"dismiss {obj}" in text:
            dismiss_temporarily(obj)
            speak_async(f"Okay, {obj} dismissed for now.")
            return

# Voice agent thread
def listen_loop():
    while True:
        key = cv2.waitKey(1)
        if key == ord('v'):
            print("🎤 Voice mode activated...")

            speak_async("Voice command activated. You can speak now.")
            handle_voice_command()

# Start listening thread
threading.Thread(target=listen_loop, daemon=True).start()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

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
        # ✅ Call voice handler directly from main thread
        threading.Thread(target=handle_voice_command, daemon=True).start()

cap.release()
cv2.destroyAllWindows()
