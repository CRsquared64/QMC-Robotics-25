from sr.robot3 import *
import math

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

def stop_front(mBoard):
    mBoard.motors[0].power = 0

def move_front(mBoard, power):
    mBoard.motors[0].power = power