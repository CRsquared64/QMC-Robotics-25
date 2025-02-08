import math

from sr.robot3 import *
import movment
import time
# back board turns forward drives
robot = Robot(wait_for_start=False)
pBoard = robot.power_board
backmBoard = robot.motor_boards["SR0UCD"]
frontmBoard = robot.motor_boards["SR0TCE"]
led = robot.kch

pBoard.outputs.power_on()  # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True

ids = []

def angle_check(angle):
    if angle > 0:
        return 1 # 1 is right
    elif angle < 0:
        return -1 # -1 is left
    else:
        return 0
def update_values(robot, current_marker_id):
    markers = robot.camera.see()
    for marker in markers:
        if marker.id == current_marker_id:
            return marker.position.distance, math.degrees(marker.position.horizontal_angle)
    return 0, 0

print("MARKER SETUP")

while True:
    markers = robot.camera.see()
    for marker in markers:
        if marker.id not in ids:
            ids.append(marker.id)
            print("Appended Marker", marker)
    if len(ids) == 3:
        print("Array Full, Waiting for Start!")
        break
thresh = 0.0005
turn_p = 0.25
drive_p = 0.5
robot.wait_start()
for i in range(3):
    for z in range(3):
        dist, angle = update_values(robot, ids[z])
        direction = angle_check(angle)
        if dist == 0 and angle == 0:
            dist, angle = update_values(robot, ids[z])
            while dist == 0 and angle == 0:
                movment.right(backmBoard, turn_p)
                dist, angle = update_values(robot, ids[z])
            movment.stop_motors(backmBoard)

        while direction == 1 and angle > thresh or direction == -1 and angle < -thresh:
            dist, angle = update_values(robot, ids[z])
            print(dist, angle)
            direction = angle_check(angle)
            if direction == 1 and angle > thresh:
                movment.right(backmBoard, turn_p)
            elif direction == -1 and angle < -thresh:
                movment.left(backmBoard, turn_p)
            else:
                movment.stop_motors(backmBoard)
                time.sleep(0.5)
                dist, angle = update_values(robot, ids[z])
                direction = angle_check(angle)
                if direction == 1 and angle < thresh or direction == -1 and angle > -thresh:
                    break
        while dist > 500:
            movment.forward(frontmBoard, drive_p)

        movment.stop_front(frontmBoard)

        # now turn to see next marker
