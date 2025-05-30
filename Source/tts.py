# tts.py
import subprocess
import threading

# Default voice (can change to 'slt' or 'rms' if you prefer)
VOICE = "kal"

def speak(text, volume=80):
    """
    Speak text using flite in a non-blocking thread.
    
    :param text: Text to speak
    :param volume: Percent volume (0-100), system level
    """
    def _speak():
        # Set system volume first (change card number if needed)
        subprocess.run(["amixer", "-c", "2", "sset", "Speaker", f"{volume}%"])
        # Speak using flite
        subprocess.Popen(["flite", "-voice", VOICE, "-t", text])
    
    # Run _speak in a background thread
    threading.Thread(target=_speak, daemon=True).start()
