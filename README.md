# 🕷️ SpideySense – Your AI-Powered Vision Assistant

SpideySense is a real-time personal safety and perception assistant that helps you stay aware of your surroundings using computer vision, audio alerts, and AI voice interaction.

> 💡 Built for joggers, commuters, and creators who want AI-powered "Spidey senses" in the real world.

---

## ⚙️ Features

| Feature                 | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| 🎯 Object Detection     | Detects objects in real-time using YOLOv8                                  |
| 📏 Distance Estimation  | Calculates how far objects are (in cm) using known dimensions               |
| 🔊 Voice Alerts         | Warns you if a person or object is too close (with direction awareness)     |
| 🎙️ Voice Command Mode  | Press `v` to ask things like "What's around me?" via Whisper + Gemini       |
| 📝 Text Input Mode      | Press `t` to type instead of speak (great when you're in quiet environments )|
| 🔕 Object Dismissal     | Press `d` or say “dismiss [object]” to mute specific objects temporarily     |
| 🛑 Easy Exit            | Press `q` anytime to quit                                                    |

---

---

## 🌟 Vision & Purpose – Why I Built SpideySense

> “I’ve always imagined having an extra pair of eyes — an AI that could sense the world around me, alert me when I’m distracted, and help me stay aware without needing to look.”

### 💭 The Problem

In today’s world, we’re often:
- Plugged into music, screens, or thoughts while walking or jogging
- Distracted in urban environments
- Unaware of real-world cues like traffic, obstacles, or people

⚠️ One moment of distraction can cost safety.

---

### 💡 The Vision

SpideySense is my attempt to build a **real-time AI-powered sixth sense**:
- 👁️ That sees what’s around me using computer vision
- 🧠 That understands context and responds intelligently
- 🗣️ That speaks to me like a companion and warns me when needed

This isn’t just object detection — it’s a **context-aware, voice-assisted safety agent** built for humans navigating a noisy, distracted world.

---

## 🔮 Future Enhancements & Roadmap

| Phase | Feature                    | Description                                                                 |
|-------|----------------------------|-----------------------------------------------------------------------------|
| ✅ 1   | YOLO + Distance Estimation | Real-time object detection + how far objects are from user                 |
| ✅ 2   | Voice Assistant            | Press `v` to ask questions like “What’s around me?” or “Dismiss person”    |
| 🚀 3   | Directional Awareness      | Voice alerts include direction (left, right, ahead)                        |
| 📝 4   | Smart Event Logger         | Auto-log past warnings with timestamps to view or summarize later          |
| 🔦 5   | Flashlight/LED Trigger     | If object too close in dark, simulate light flash or activate hardware     |
| 🛰️ 6   | GPS Location Awareness     | Warn user about intersections, danger zones (future mobile support)        |
| 🦿 7   | Wearable Deployment        | Run on Jetson Nano, ESP32, or RPi for outdoor/portable use                 |
| 🤕 8   | Fall Detection + Help Mode | If fall is detected + voice says "help" → auto trigger emergency protocol  |
| 📡 9   | Audio Command Triggers     | Run automations from voice like "record video" or "send my location"       |

---

## 🚀 Ultimate Goal

To build **AI companions that augment human perception** —  
making everyday navigation **smarter, safer, and more situationally aware.**

> 🕷️ SpideySense is not just a project — it’s the beginning of voice-aware vision agents for real-world interaction.
---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/SpideySense.git
cd SpideySense
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the assistant
```bash
python main.py
```
✅ Make sure your webcam is connected
✅ Press v to ask questions
✅ Press d to dismiss a detected object
✅ Press t to type instead of talk
✅ Press q to exit anytime

<hr>

## 🧠 Powered By
- YOLOv8 – Object Detection


- OpenAI Whisper – Speech Recognition


- Gemini API – AI Brain


- pyttsx3 – Text-to-Speech (offline)


## Project Structure
```bash
SpideySense/
│
├── main.py                      # Main app
├── requirements.txt             # All dependencies
├── README.md                    # This file
│
├── object_detector/
│   ├── yolo_detector.py
│   └── distance_estimator.py
│
└── voice_agent/
    ├── stt_whisper.py
    ├── tts_robotic.py
    └── ai_brain.py
```

### 🌟 Future Upgrades
- 🧭 Directional awareness in voice alerts

- 📝 Auto event logging & summarization

- 🔦 Flashlight / LED trigger if too close

- 🧠 Real-world integration via mobile/ESP32

  more soon (look out for v2)
