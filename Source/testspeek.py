import subprocess
import threading

def speak(text):
    subprocess.Popen(["flite", "-voice", "slt", "-t", text])

# Main loop
print("Doing other work...")

threading.Thread(target=speak, args=("Hello humans, I am 80-HD!",), daemon=True).start()

for i in range(10):
    print(f"Main loop iteration {i}")
    import time
    time.sleep(0.5)
