import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

#Define global parameters
SPEED = 1


def initialize_motors():
    board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)  #
    board.enable_reception(True)
    return board

def main():
    board = initialize_motors()

if __name__ == '__main__':
    main()