from sr.robot3 import *
import time
import math
import movment
import numpy as np


import math

power = 0.6 # power of motors

robot = Robot() # get robot object
pBoard = robot.power_board
backmBoard = robot.motor_boards["SR0UCD"]
frontmBoard = robot.motor_boards["SR0TCE"]

pBoard.outputs.power_on() # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True

arduino = robot.arduino

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

def update_heading(arduino_angle, turn_angle, direction):
    return (arduino_angle + turn_angle * direction) % 360
def average_angle(arduino):
    angles = []
    for i in range(1, 10):
        angles.append(float(arduino.command('c')))
    mean_angle = sum(angles) // 10
    return mean_angle


def turn_amount(current, target):
    difference = (target - current) % 360  # Get the difference in the range [0, 360)
    if difference > 180:  # Take the shorter negative route if > 180
        difference -= 360

    direction = 1 if difference > 0 else -1  # 1 for right -1 for left
    return abs(difference), direction
def ArduinoDrive(robot, marker, power, backmBoard, frontmBoard, arduino):
    distance, angle = update_values(robot, marker)
    direction = angle_check(angle)
    arduino_angle = average_angle(arduino)
    print(f"Actual Angle: {angle}, Arduino Angle: {arduino_angle}")
    updated_heading = update_heading(arduino_angle, angle, direction)
    while distance > 20:
        arduino_angle = average_angle(arduino)
        difference, direction = turn_amount(arduino_angle, updated_heading)
        print(f"Target Heading {updated_heading}, Arduinos Heading {average_angle(arduino)}")
        print(f"Difference: {difference}, Distance{distance}")
        if difference > 2:
            if direction == 1:
                movment.right(backmBoard, 0.3)
            else:
                movment.left(backmBoard, 0.3)
        else:
            movment.stop_motors(backmBoard)

        if distance > 20:
            movment.forward(frontmBoard, 0.5)
        else:
            movment.stop_front(frontmBoard)
        temp_distance, _ = update_values(robot, marker)
        if temp_distance != 0:
            distance = temp_distance
        time.sleep(0.01)

        """
        print(f"Target Heading {updated_heading}, Arduinos Heading {average_angle(arduino)}")
        if updated_heading > average_angle(arduino):
            movment.right(backmBoard, 0.3)
            print("right")
        elif updated_heading < average_angle(arduino):
            movment.left(backmBoard, 0.3)
            print("left")
        if updated_heading - 10 < average_angle(arduino) < updated_heading + 10:
            movment.stop_motors(backmBoard)
        """






while True:
    markers = robot.camera.see()
    if markers:
        for marker in markers:
            print(f"[Marker: {marker.id}] Spotted")
        time.sleep(1)  # wait before moving for demonstartion
        current_marker = markers[0]  # go for the first one it sees (not closest)
        print(f"Driving to marker {current_marker.id}")
        while True:
            ArduinoDrive(robot, current_marker, power ,backmBoard, frontmBoard, arduino)
        break