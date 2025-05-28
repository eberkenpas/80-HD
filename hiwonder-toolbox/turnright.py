import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)  #
board.enable_reception(True)

print("Battery:", board.get_battery())
import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)  #
board.enable_reception(True)

speed = -1

print("IMU: ", board.get_imu())
board.set_motor_speed([[1,speed]]) #Spin Right Front wheel
board.set_motor_speed([[2,speed]]) #spin right rear wheel
board.set_motor_speed([[3,speed]]) #spin left front wheel
board.set_motor_speed([[4,speed]]) #spin left rear wheel

