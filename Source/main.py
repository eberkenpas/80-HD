import tts
import random
import time
import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

SPEED = 1
STOP = 0

def initialize_motors():
    board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)
    board.enable_reception(True)
    return board

def main():
    board = initialize_motors()
    
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
    
    tts.speak_blocking("I will now test my abilities.", volume=80)

    #Test Code
    directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
    for i in range(20):
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
