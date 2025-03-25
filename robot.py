# this is too short notice
# if this works you all owe me big time

from sr.robot3 import *
import time

from guidance import Guidance
from motion import Motion
from interactionSuite import InteractionSuite


class RobotHandler:
    POWER = 1
    INCLUDE = [x for x in range(0,300)] # what markers do we want vroskis
    THRESH = 5 # wiggle room - wiggle wiggle wiggle

    IRCCM_TIMEOUT = 2# how long we ignore motionblur
    MIN_DIST = 50 # when to stop the robot before hitting? if we do?
    def __init__(self, frontMotor, backMotor, ):
        self.robot = Robot()
        self.pBoard = self.robot.power_board
        self.frontMotor = frontMotor
        self.backMotor = backMotor

        self.pBoard.outputs.power_on()  # turn on pBoard
        self.pBoard.outputs[OUT_H0].is_enabled = True

        self.arduino = self.robot.arduino

        self.Guidance = Guidance(self.robot)
        self.Motion = Motion()
        self.InteractionSuite = InteractionSuite()



    def lock_target(self):
        target_marker = False
        while not target_marker:
            target_marker = self.Guidance.get_marker(self.robot, self.INCLUDE)
        print(f"[TARGET ACQUIRED]: {target_marker.id} Dist: {target_marker.position.distance}")
        angle, dist = self.Guidance.movement_calculate(target_marker)
        self.start_guidance(angle,dist, target_marker)
    def start_guidance(self, angle, dist, target_marker):
        ready_for_sucking = False
        while True:
            if dist <= self.MIN_DIST:
                ready_for_sucking = True
                break
            direction = self.Guidance.angle_check(angle)
            if direction != 0: # only zero if it cant see it anymore
                if direction == 1 and angle > self.THRESH:
                    self.Motion.right(self.backMotor, self.POWER)
                    time.sleep(0.05)
                    print("Right")
                    turned = True

                if direction == 1 and angle < -self.THRESH:
                    self.Motion.left(self.backMotor, self.POWER)
                    time.sleep(0.05)
                    print("Left")
                    turned = True
                self.Motion.forward(self.frontMotor, self.POWER)
                self.Motion.forward(self.backMotor, self.POWER) # this will cause it to jitter

            else: # go dead forward on slow speed and scan like hell
                self.Motion.forward(self.frontMotor, self.POWER / 2)
                self.Motion.forward(self.backMotor, self.POWER / 2 )
                if self.Guidance.IRCCM(self.IRCCM_TIMEOUT, target_marker):
                    pass # if we relock, continue BITCHES
                else:
                    break # get out the loop

            angle, dist = self.Guidance.movement_calculate(target_marker)

        if ready_for_sucking:
            self.pickup_procedure()
        else:
            self.lock_target()

    def pickup_procedure(self):
        pass