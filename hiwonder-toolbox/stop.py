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

print("IMU: ", board.get_imu())

board.set_motor_speed([[1,0]]) #Spin Right Front wheel
board.set_motor_speed([[2,0]]) #spin right rear wheel
board.set_motor_speed([[3,0]]) #spin left front wheel
board.set_motor_speed([[4,0]]) #spin left rear wheel

pos = board.bus_servo_read_position(1)
print("Servo 1 position:", pos)
