import tts
import random
import time
import sys
import speech_recognition as sr
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk
import subprocess

SPEED = 1
STOP = 0

def initialize_motors():
    board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)
    board.enable_reception(True)
    return board

def initialize_speech_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        recognizer.adjust_for_ambient_noise(source)
    return recognizer

def speak_introduction():
    # Greet at startup!
    tts.speak_blocking("Hello, I am 80 H D. ", volume=80)

    #pause for 1 second
    time.sleep(1)

    tts.speak_blocking("I am a robot created by Ella Mae Berkenpas.", volume=80)

    #pause for 1 second
    time.sleep(1)

    tts.speak_blocking("I am Ella's 5th grade strengths project.", volume=80)

    #pause for 1 second
    time.sleep(1)
    
    tts.speak_blocking("Please tell me what you want to do.", volume=80)
    time.sleep(1)

def main():
    #Set Master Volume to 80%
    subprocess.run(['amixer', 'sset', 'Master', '80%'])

    # Initialize the speech recognition
    recognizer = initialize_speech_recognition()

    # Initialize the motors
    board = initialize_motors()
    
    speak_introduction()

    while True:
        # Listen for user input
        with sr.Microphone(device_index=2) as source:
            print("Listening...")
            tts.speak_blocking("I am listening")
            audio = recognizer.listen(source)

        # Recognize speech
        try:
            print("Recognizing (offline)...")
            text = recognizer.recognize_sphinx(audio)
            print("You would like me to:", text)
            tts.speak_blocking(f"You would like me to: {text}", volume=80)
        except sr.UnknownValueError:
            print("Could not understand audio.")
            tts.speak_blocking("I did not understand you. Please try again.", volume=80)
            continue
        except sr.RequestError as e:
            print("PocketSphinx error:", e)
            tts.speak_blocking("I did not understand you. Please try again.", volume=80)
            continue

        # Process user command with default being "I do not know how to do that"
        if text.lower() == "go":
            tts.speak_blocking("Ok, I will go.", volume=80)
            time.sleep(1)
        if text.lower() == "hello":
            tts.speak_blocking("Ok, I will say hello.", volume=80)
            time.sleep(1)
            tts.speak_blocking("Hello, how are you?", volume=80)
            time.sleep(1)
        if text.lower() == "talk to me":
            tts.speak_blocking("Ok, I will talk to you.")
            time.sleep(1)
            tts.speak_blocking("I am testing my abilities. I am 80 HD")
            time.sleep(1)
        if text.lower() == "lucy":
            tts.speak_blocking("Ok, I will Lucy.")
            time.sleep(1)
            tts.speak_blocking("Bark! Bark! Bark!")
            time.sleep(1)
        else:
            tts.speak_blocking("I do not know how to do that.", volume=80)

    tts.speak_blocking("I will now test my abilities.")

    #Test Code
    directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
    for i in range(5):
        direction = random.choice(directions)
        tts.speak(f"Moving {direction}.", volume=80)
        
        if direction == 'forward':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])
        elif direction == 'backward':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])
        elif direction == 'left':
            board.set_motor_speed([[1, SPEED], [2, -SPEED], [3, SPEED], [4, -SPEED]])
        elif direction == 'right':
            board.set_motor_speed([[1, -SPEED], [2, SPEED], [3, -SPEED], [4, SPEED]])
        elif direction == 'turn left':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, SPEED], [4, SPEED]])
        elif direction == 'turn right':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, -SPEED], [4, -SPEED]])
        
        time.sleep(1)
        board.set_motor_speed([[1, STOP], [2, STOP], [3, STOP], [4, STOP]])
        time.sleep(0.5)

    tts.speak_blocking("Test complete.", volume=80)

if __name__ == '__main__':
    main()
