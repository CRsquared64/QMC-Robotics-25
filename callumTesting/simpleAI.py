from sr.robot3 import *
import time
import math
import movment
power = 0.4 # power of motors

robot = Robot() # get robot object
pBoard = robot.power_board
mBoard = robot.motor_board

pBoard.outputs.power_on() # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True

markers = None

def angle_check(angle):
    if angle > 0:
        return 1 # 1 is right
    elif angle < 0:
        return -1 # -1 is left
    else:
        return 0

def update_values(robot, current_marker):
    markers = robot.camera.see()
    for marker in markers:
        if marker.id == current_marker.id:
            return marker.position.distance, math.degrees(marker.position.horizontal_angle)
    return 0,0


def drive_to_marker(robot, marker, power, mBoard):
    distance, angle = update_values(robot, marker)
    direction = angle_check(angle)
    if direction != 0: # if it can actually see it basically
        if direction == 1:
            movment.stop_motors(mBoard)
            movment.right(mBoard, power + 0.2)
            time.sleep(0.1)
        else:
            movment.stop_motors(mBoard)
            movment.left(mBoard, power + 0.2)
            time.sleep(0.1)
        if distance != 0:
            movment.forward(mBoard, power)
    else:
        movment.stop_motors(mBoard)
        time.sleep(1)









while True:
    markers = robot.camera.see()
    if markers:
        for marker in markers:
            print(f"I see Marker {marker.id} at {marker.position.distance}M")
        time.sleep(1) # wait before moving for demonstartion
        current_marker = markers[0] # go for the first one it sees (not closest)
        print(f"Driving to marker {current_marker.id}")
        while True:
            drive_to_marker(robot, current_marker, power, mBoard)
        break






