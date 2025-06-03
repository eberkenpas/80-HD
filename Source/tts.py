# tts.py
import subprocess
import threading

# Default voice
#VOICE = "kal"  # or "slt", "rms", "awb"
VOICE = "slt"  # or "slt", "rms", "awb"

def speak(text, volume=80):
    """
    Non-blocking: Speak text in background thread.
    
    :param text: Text to speak
    :param volume: Volume % (0-100)
    """
    def _speak():
        subprocess.run(["amixer", "-c", "2", "sset", "Speaker", f"{volume}%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["flite", "-voice", VOICE, "-t", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    threading.Thread(target=_speak, daemon=True).start()

def speak_blocking(text, volume=80):
    """
    Blocking: Speak text and wait until done.
    
    :param text: Text to speak
    :param volume: Volume % (0-100)
    """
    subprocess.run(["amixer", "-c", "2", "sset", "Speaker", f"{volume}%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["flite", "-voice", VOICE, "-t", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
