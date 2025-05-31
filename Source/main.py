import tts
import random
import time
import sys
import difflib
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

def explore(board):
    #Test Code
    directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
    for i in range(5):
        direction = random.choice(directions)
        tts.speak(f"Moving {direction}.")
        
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


def main():
    #Set Master Volume to 80%
    print("Setting Master Volume to 80%")
    subprocess.run(['amixer', 'sset', 'Master', '80%'])

    time.sleep(1)

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
            time.sleep(1)
            audio = recognizer.listen(source)

        # Recognize speech
        try:
            print("Recognizing (offline)...")
            text = recognizer.recognize_sphinx(audio)
            print("Text:", text)

            # Make a list of words and find the one that is closest to the command list
            command_list = ["go", "explore", "hello", "talk to me", "lucy"]
            #make a list of the words in the text
            text_words = text.lower().split()
            # Check if the list for the closest word to the command list prioritizing the first command if there are two matches
            closest_word = difflib.get_close_matches(text_words, command_list, n=1, cutoff=0.4)
            print(f"Closest word: {closest_word}")
            if closest_word:
                text = closest_word[0]
                print(f"Closest word: {closest_word}")
                print("You would like me to:", text)
                tts.speak_blocking(f"You would like me to: {text}")
            else:
                print("No close match found.")
                tts.speak_blocking("I did not understand you. Please try again.")
                continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
            tts.speak_blocking("I did not understand you. Please try again.")
            continue
        except sr.RequestError as e:
            print("PocketSphinx error:", e)
            tts.speak_blocking("I did not understand you. Please try again.")
            continue

        # Process user command with default being "I do not know how to do that"
        if text.lower() == "go":
            tts.speak_blocking("Ok, I will go explore.")
            time.sleep(1)
            explore(board)            
        if text.lower() == "explore":
            tts.speak_blocking("Ok, I will go explore.")
            time.sleep(1)
            explore(board)
        if text.lower() == "hello":
            tts.speak_blocking("Ok, I will say hello.")
            time.sleep(1)
            tts.speak_blocking("Hello, how are you?")
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

    tts.speak_blocking("I will now test my abilities.")

    
    tts.speak_blocking("Test complete.", volume=80)

if __name__ == '__main__':
    main()
