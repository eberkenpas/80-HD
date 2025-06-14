import tts
import random
import time
import sys
import difflib
import speech_recognition as sr
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk
import subprocess

#wait for 60 seconds for the microphones to be ready
#time.sleep(60)

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
    tts.speak_blocking("Hello, I am 80 H D.", volume=80)

    #pause for 1 second
    time.sleep(1)

    tts.speak_blocking("I am a robot created by Ella Mae Berkenpas.", volume=80)

    #pause for 1 second
    time.sleep(1)

    tts.speak_blocking("I am Ella's 5th grade strengths project.", volume=80)

    #pause for 1 second
    time.sleep(1)
    
    #tts.speak_blocking("Please tell me what you want to do.", volume=80)
    time.sleep(1)

# def explore(board):
#     #Test Code
#     directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
#     for i in range(5):
#         direction = random.choice(directions)
#         tts.speak(f"Moving {direction}.")
        
#         if direction == 'forward':
#             board.set_motor_speed([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])
#         elif direction == 'backward':
#             board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])
#         elif direction == 'left':
#             board.set_motor_speed([[1, SPEED], [2, -SPEED], [3, SPEED], [4, -SPEED]])
#         elif direction == 'right':
#             board.set_motor_speed([[1, -SPEED], [2, SPEED], [3, -SPEED], [4, SPEED]])
#         elif direction == 'turn left':
#             board.set_motor_speed([[1, SPEED], [2, SPEED], [3, SPEED], [4, SPEED]])
#         elif direction == 'turn right':
#             board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, -SPEED], [4, -SPEED]])
        
#         time.sleep(1)
#         board.set_motor_speed([[1, STOP], [2, STOP], [3, STOP], [4, STOP]])
#         time.sleep(0.5)

def explore(board):
    directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
    move_history = []

    # Forward moves
    for i in range(7):
        direction = random.choice(directions)
        move_history.append(direction)

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

    # Going back
    tts.speak_blocking("That was so much fun. No I must return home.")

    reverse_map = {
        'forward': 'backward',
        'backward': 'forward',
        'left': 'right',
        'right': 'left',
        'turn left': 'turn right',
        'turn right': 'turn left'
    }

    for direction in reversed(move_history):
        reverse_direction = reverse_map[direction]
        tts.speak(f"Moving {reverse_direction}.")
        
        if reverse_direction == 'forward':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])
        elif reverse_direction == 'backward':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])
        elif reverse_direction == 'left':
            board.set_motor_speed([[1, SPEED], [2, -SPEED], [3, SPEED], [4, -SPEED]])
        elif reverse_direction == 'right':
            board.set_motor_speed([[1, -SPEED], [2, SPEED], [3, -SPEED], [4, SPEED]])
        elif reverse_direction == 'turn left':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, SPEED], [4, SPEED]])
        elif reverse_direction == 'turn right':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, -SPEED], [4, -SPEED]])
        
        time.sleep(1)
        board.set_motor_speed([[1, STOP], [2, STOP], [3, STOP], [4, STOP]])
        time.sleep(0.5)

    tts.speak_blocking("My adventure is complete.  I have so many wonderful stories to tell.")


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

    failed_attempts = 0

    # Loop until user says quit
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
            command_list = ["go", "explore", "hello", "talk", "lucy", "dog", "quit", "shutdown", "off"]
            #make a list of the words in the text
            text_words = text.lower().split()
            # Check if the list for the closest word to the command list prioritizing the first command if there are two matches
            matches = []
            for word in text_words:
                match = difflib.get_close_matches(word, command_list, n=1, cutoff=0.6)
                if match:
                    matches.append(match[0])

            if matches:
                text = matches[0]

            print(f"Closest word: {text}")
            if text and matches:
                print(f"Closest word: {text}")
                print("You would like me to:", text)
                tts.speak_blocking(f"You would like me to: {text}")
                failed_attempts = 0
            else:
                print("No close match found.")
                tts.speak_blocking("I did not understand you. Please try again.")
                failed_attempts += 1
                if failed_attempts >= 4:
                    tts.speak_blocking("I am bored.  I think I will go explorer.")
                    explore(board)
                continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
            tts.speak_blocking("I did not understand you. Please try again.")
            failed_attempts += 1
            if failed_attempts >= 4:
                tts.speak_blocking("I am bored.  I think I will go explorer.")
                explore(board)
            continue
        except sr.RequestError as e:
            print("PocketSphinx error:", e)
            tts.speak_blocking("I did not understand you. Please try again.")
            failed_attempts += 1
            if failed_attempts >= 4:
                tts.speak_blocking("I am bored.  I think I will go explorer.")
                explore(board)
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
        if text.lower() == "talk":
            tts.speak_blocking("Ok, I will talk to you.")
            time.sleep(1)
            tts.speak_blocking("I am testing my abilities. I am 80 HD")
            time.sleep(1)
        if text.lower() == "lucy":
            tts.speak_blocking("Ok, I will Lucy.")
            time.sleep(1)
            tts.speak_blocking("Bark! Bark! Bark!")
            time.sleep(1)
        if text.lower() == "dog":
            tts.speak_blocking("Ok, I will bark like a dog.")
            time.sleep(1)
            tts.speak_blocking("Bark! Bark! Bark!")
            time.sleep(1)
        if text.lower() in ["quit", "shutdown", "off"]:
            tts.speak_blocking("Ok, I will shut down.")
            time.sleep(1)
            break

    
    tts.speak_blocking("The test is complete. Don't forget to push the little white button and wait for the red light to come on.", volume=80)
    time.sleep(1)
    tts.speak_blocking("Oh I almost forgot. You should probably charge my batteries. Goodbye.")
    time.sleep(1)

if __name__ == '__main__':
    main()
 