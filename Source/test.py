import sys
sys.path.append('/home/pi/hiwonder-toolbox')
import ros_robot_controller_sdk as sdk

board = sdk.Board(device='/dev/ttyACM0', baudrate=1000000)  #
board.enable_reception(True)

print("IMU: ", board.get_imu())

pos = board.bus_servo_read_position(1)
print("Servo 1 Position:", pos)

