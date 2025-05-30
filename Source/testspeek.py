import pyttsx3
import threading

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()  # blocking INSIDE this thread

# Main program
print("Doing other work...")

# Start TTS in background
threading.Thread(target=speak, args=("Hello humans, I am 80-HD!",), daemon=True).start()

# Meanwhile, keep doing other stuff
for i in range(10):
    print(f"Main loop iteration {i}")
    import time
    time.sleep(0.5)
