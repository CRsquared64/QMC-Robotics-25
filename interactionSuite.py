from sr.robot3 import *
import time

class InteractionSuite:
    def __init__(self, robot, pboard, sboard):
        self.robot = robot
        self.pBoard = pboard
        self.sBoard = sboard
        self.sBoard.servos[7].set_duty_limits(1056, 2000)

    def activate_solenoid(self):
        self.pBoard.outputs[OUT_L1].is_enabled = True

    def deactivate_solenoid(self):
        self.pBoard.outputs[OUT_L1].is_enabled = False

    def suck_solenoid_activ(self):
        self.pBoard.outputs[OUT_L3].is_enabled = True

    def suck_solenoid_deactiv(self):
        self.pBoard.outputs[OUT_L3].is_enabled = False


    def arm_down(self):
        self.sBoard.servos[7].position = -1

    def arm_up(self):
        self.sBoard.servos[7].position = 1

    def arm_centre(self):
        self.sBoard.servos[7].position = 0

    def main_arm_down(self, mBoard, arduino):
        mBoard.motors[1].power = 0.2
        #time.sleep(0.5)
        while True:
            check = int(arduino.command("d"))
            print(check)
            if not check:
                print("ARM DOWN")
                mBoard.motors[1].power = 0
                break



    def main_arm_up(self, mBoard, arduino):
        mBoard.motors[1].power = -0.5
        #time.sleep(0.7)
        while True:
            check = int(arduino.command("u"))
            if not check:
                print("ARM UP")
                mBoard.motors[1].power = 0
                break

    def suck_hard(self, mBoard):
        self.suck_solenoid_deactiv()
        mBoard.motors[0].power = 1
        print("SUCKING")

    def release(self, mBoard):
        mBoard.motors[0].power = 0
        self.suck_solenoid_activ()
        time.sleep(0.5)
        self.suck_solenoid_deactiv()

    def is_sucking(self, arduino):
        sums_arr = 0
        n_steps = 100
        for i in range(n_steps):
            sums_arr += int(arduino.command("z"))
        mean = sums_arr / n_steps
        if mean >= 0.90:
            return False
        else:
            return True