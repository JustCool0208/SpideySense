import whisper

model = whisper.load_model("base")

def transcribe():
    print("🎙️ Listening...")
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile

    duration = 5
    fs = 16000
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    scipy.io.wavfile.write("temp.wav", fs, audio)

    result = model.transcribe("temp.wav")
    return result["text"].strip()
