import tts
import random
import time
import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

SPEED = 1

def initialize_motors():
    board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)
    board.enable_reception(True)
    return board

def main():
    board = initialize_motors()
    
    # Greet at startup!
    tts.speak_blocking("Hello, I am 80 H D. Initializing motors.", volume=80)
    
    directions = ['forward', 'backward', 'left', 'right', 'turn left', 'turn right']
    for i in range(20):
        direction = random.choice(directions)
        tts.speak(f"Moving {direction}.", volume=80)
        
        if direction == 'forward':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, -SPEED], [4, -SPEED]])
        elif direction == 'backward':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, SPEED], [4, SPEED]])
        elif direction == 'left':
            board.set_motor_speed([[1, -SPEED], [2, SPEED], [3, -SPEED], [4, SPEED]])
        elif direction == 'right':
            board.set_motor_speed([[1, SPEED], [2, -SPEED], [3, SPEED], [4, -SPEED]])
        elif direction == 'turn left':
            board.set_motor_speed([[1, SPEED], [2, SPEED], [3, SPEED], [4, SPEED]])
        elif direction == 'turn right':
            board.set_motor_speed([[1, -SPEED], [2, -SPEED], [3, -SPEED], [4, -SPEED]])
        
        time.sleep(1)
        board.set_motor_speed([[1, 0], [2, 0], [3, 0], [4, 0]])
        time.sleep(0.5)

if __name__ == '__main__':
    main()
