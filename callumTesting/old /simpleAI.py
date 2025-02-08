from sr.robot3 import *
import time
import math
import movment

power = 0.6 # power of motors

robot = Robot() # get robot object
pBoard = robot.power_board
backmBoard = robot.motor_boards["SR0UCD"]
frontmBoard = robot.motor_boards["SR0TCE"]

pBoard.outputs.power_on() # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True
thresh = 3
markers = None

angle_factor = 6


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


def drive_to_marker(robot, marker, power, backmBoard, frontmBoard):
    turned = False
    turn_power = 0.9
    distance, angle = update_values(robot, marker)
    print(f"Distance {distance}, Angle {angle}, Power {power}")
    direction = angle_check(angle)
    if direction != 0: # if it can actually see it basically
        if direction == 1 and angle > thresh:
            movment.right(backmBoard, turn_power )
            time.sleep(0.05)
            print("Going Right")
            turned = True
        elif direction == -1 and angle < -thresh:
            movment.left(backmBoard, turn_power)
            print("Going Left")
            time.sleep(0.05)
            turned = True
        movment.move_front(frontmBoard, power)
        movment.forward(backmBoard, power)
        time.sleep(0.3)
        if turned:
            time.sleep(0.2)
            print("stop")
    else:
        movment.stop_motors(backmBoard)
        movment.stop_front(frontmBoard)
    prev_distance, prev_angle = distance, angle



while True:
    markers = robot.camera.see()
    if markers:
        for marker in markers:
            print(f"I see Marker {marker.id} at {marker.position.distance}mm")
        time.sleep(1) # wait before moving for demonstartion
        current_marker = markers[0] # go for the first one it sees (not closest)
        print(f"Driving to marker {current_marker.id}")
        while True:
            drive_to_marker(robot, current_marker, power, backmBoard, frontmBoard)
        break


time.now()