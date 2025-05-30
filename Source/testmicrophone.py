import speech_recognition as sr

def listen_offline():
    recognizer = sr.Recognizer()
    
    # Use USB card 2 or 3
    mic = sr.Microphone(device_index=2)  # Try 2 or 3 depending on which mic is plugged in
    
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

# Test
listen_offline()
