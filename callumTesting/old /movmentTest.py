from sr.robot3 import *
import time

robot = Robot()

power = 0.5

pBoard = robot.power_board
mBoard = robot.motor_boards["SR0TCE"]

pBoard.outputs.power_on() # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True

def stop_motors(mBoard):
    for m in mBoard.motors:
        m.power = 0
while True:
    time.sleep(1)
    print("Test 1") # right
    mBoard.motors[0].power = power
    mBoard.motors[1].power = power
    time.sleep(0.5)
    stop_motors(mBoard)
    time.sleep(0.5)
    print("Test 2") # left
    mBoard.motors[0].power = -power
    mBoard.motors[1].power = -power
    time.sleep(0.5)
    stop_motors(mBoard)
    time.sleep(0.5)
    print("Test 3") # foward
    mBoard.motors[0].power = -power
    mBoard.motors[1].power = power
    time.sleep(0.5)
    stop_motors(mBoard)
    time.sleep(0.5)
    print("Test 4") # backwards
    mBoard.motors[0].power = power
    mBoard.motors[1].power = -power
    time.sleep(0.5)
    stop_motors(mBoard)
    time.sleep(0.5)
