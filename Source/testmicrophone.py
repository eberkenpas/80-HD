import speech_recognition as sr

recognizer = sr.Recognizer()

# List devices so you can check which number is USB mic
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Device {i}: {name}")

# After checking list, set the correct device index
mic = sr.Microphone(device_index=2, sample_rate=48000)  # Update device_index as needed

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
