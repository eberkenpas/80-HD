import speech_recognition as sr

recognizer = sr.Recognizer()

# Use Device 0 — your USB mic
mic = sr.Microphone(device_index=0, sample_rate=16000)

with mic as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Listening... Speak now!")
    audio = recognizer.listen(source)

try:
    print("Recognizing (offline)...")
    text = recognizer.recognize_sphinx(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio.")
except sr.RequestError as e:
    print("PocketSphinx error:", e)
