from sr.robot3 import *

def forward(mBoard, power):
    mBoard.motors[0].power = power
    mBoard.motors[1].power = -power

def backwards(mBoard, power):
    mBoard.motors[0].power = -power
    mBoard.motors[1].power = power

def right(mBoard, power):
    mBoard.motors[0].power = -power
    mBoard.motors[1].power = -power

def left(mBoard, power):
    mBoard.motors[0].power = power
    mBoard.motors[1].power = power

def stop_motors(mBoard):
    for m in mBoard.motors:
        m.power = 0