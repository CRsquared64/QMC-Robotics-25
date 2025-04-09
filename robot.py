# this is too short notice
# if this works you all owe me big time

from sr.robot3 import *
import time

from guidance import Guidance
from motion import Motion
from interactionSuite import InteractionSuite

import positions
#from simulator.controllers.usercode_runner.usercode_runner import robot


class RobotHandler:
    POWER = 0.5 # what markers do we want vroskis
    THRESH = 0.1  # wiggle room - wiggle wiggle wiggle

    IRCCM_TIMEOUT = 2  # how long we ignore motion blur
    MIN_DIST = 400  # when to stop the robot before hitting?

    ARDUINO_MIN = 40 # min distance before arduino switches off
    ARDUINO_TIMEOUT = 10  # how long arduino will drive before giving up
    ARDUINO_POWER = 0.225  # speed for arduino

    SUCK_TIMEOUT = 5 # how long we suck

    SEARCH_TIME = 0.3 # how long we go before scanning for next target in lock

    def __init__(self):
        self.robot = Robot(wait_for_start=False)
        self.pBoard = self.robot.power_board
        self.sBoard = self.robot.servo_board
        self.wheelMotor = self.robot.motor_boards["SR0TCE"]
        self.armPumpMotor = self.robot.motor_boards["SR0UCD"]
        self.arduino = self.robot.arduino

        self.pBoard.outputs.power_on()  # turn on pBoard
        self.pBoard.outputs[OUT_H0].is_enabled = True

        self.arduino = self.robot.arduino

        self.Guidance = Guidance(self.robot)
        self.Motion = Motion()
        self.InteractionSuite = InteractionSuite(self.robot, self.pBoard, self.sBoard)

        self.current_blocks = 0
        self.zone = 0
        self.zone_bound, self.high_rise, self.zone_pallets = positions.zone_parse(self.zone)

    def lock_target(self):
        search_target = self.zone_pallets
        print(self.current_blocks)
        if self.current_blocks >= 2:
            print("RETURNING")
            search_target = self.high_rise
        target_marker = False
        rescan_time = time.time() + self.SEARCH_TIME
        while not target_marker:
            target_marker = self.Guidance.get_marker(self.robot, search_target)
            if target_marker:
                break
            if time.time() >= rescan_time: # if we see no markers for search_time, move
                print("No Target Found, Moving to search")
                self.Motion.right(self.wheelMotor, 0.5)
                time.sleep(0.4)
                self.Motion.stop_motors(self.wheelMotor)
                rescan_time = time.time() + self.SEARCH_TIME
                print("STILL SEARCHING")
        print(f"[TARGET ACQUIRED]: {target_marker.id} Dist: {target_marker.position.distance}")
        dist, angle = self.Guidance.update_values(self.robot, target_marker)  # get starting positions
        print(angle, dist)
        self.start_guidance(angle, dist, target_marker)

    def start_guidance(self, angle, dist, target_marker):
        if not target_marker:
            self.lock_target()
        ready_for_sucking = False
        while True:
            if dist <= self.MIN_DIST and dist != 0: # if we are within sucking range
                print(dist, self.MIN_DIST)
                ready_for_sucking = True
                break
            direction = self.Guidance.angle_check(angle) # returns left or right
            print(direction)
            if direction != 0:  # only zero if it cant see it anymore
                if direction == 1 and angle > self.THRESH:
                    self.Motion.right(self.wheelMotor, self.POWER + 0.4)
                    time.sleep(0.03)
                    print("Right")
                    turned = True

                if direction == -1 and angle < -self.THRESH:
                    self.Motion.left(self.wheelMotor, self.POWER + 0.4)
                    time.sleep(0.03)
                    print("Left")
                    turned = True
                self.Motion.forward(self.wheelMotor, self.POWER)

            else:  # go dead forward on slow speed and scan like hell
                self.Motion.forward(self.wheelMotor, self.POWER / 3)
                print("IRCCM ACTIVE")
                if self.Guidance.IRCCM(self.IRCCM_TIMEOUT, target_marker):
                    print("Target Reacquired")  # if we relock, continue BITCHES
                else:
                    print("Lost Target")
                    break  # get out the loop

            dist, angle = self.Guidance.update_values(self.robot, target_marker)
            print(angle, dist)
        print(target_marker)
        print(self.high_rise)

        if ready_for_sucking and target_marker.id not in self.high_rise:
            self.Motion.stop_motors(self.wheelMotor)
            self.pickup_procedure()
        elif ready_for_sucking and target_marker.id in self.high_rise:
            print("DROPPING BLOCKS")
            self.Motion.stop_motors(self.wheelMotor)
            self.InteractionSuite.arm_up()
            self.InteractionSuite.activate_solenoid()
            self.robot.sleep(1)
            self.Motion.backwards(self.wheelMotor, 0.3)
            self.robot.sleep(6)
            self.Motion.stop_motors(self.wheelMotor)
            self.InteractionSuite.arm_down()
            self.InteractionSuite.deactivate_solenoid()
            self.current_blocks = 0
            self.lock_target()

        else:
            self.lock_target()

    def pickup_procedure(self):
        if self.arduino_drive():
            print("Arm Down")
            self.InteractionSuite.main_arm_down(self.armPumpMotor, self.arduino) #moves arm down
            print("Sucking")
            self.InteractionSuite.suck_solenoid_deactiv()
            self.InteractionSuite.suck_hard(self.armPumpMotor)
            time.sleep(0.2)
            end = time.time() + self.SUCK_TIMEOUT
            while time.time() < end:
                if self.InteractionSuite.is_sucking(self.arduino):
                    print("WE HAVE SUCK")
                    self.current_blocks += 1 # if its sucking, assume we hav eblock
                    break
                time.sleep(0.2)
            # routine below deposits block regardless if we have it, nessecary
            self.InteractionSuite.main_arm_up(self.armPumpMotor, self.arduino)
            #self.InteractionSuite.arm_centre()
            time.sleep(3)
            print("RELEASE")
            self.InteractionSuite.release(self.armPumpMotor)
            time.sleep(1)
            #self.InteractionSuite.arm_down()
            self.Motion.backwards(self.wheelMotor, 0.2)
            time.sleep(1)
            self.Motion.stop_motors(self.wheelMotor)
            self.lock_target()

        else:
            self.lock_target()

    def arduino_drive(self):
        end_time = time.time() + self.ARDUINO_TIMEOUT
        while True:
            self.Motion.forward(self.wheelMotor, self.ARDUINO_POWER)
            dist = self.Guidance.get_arduino_distance(self.arduino)
            if dist <= self.ARDUINO_MIN:
                self.robot.sleep(1)
                self.Motion.stop_motors(self.wheelMotor)
                return True
            elif time.time() >= end_time:
                self.Motion.stop_motors(self.wheelMotor)
                return False

    def return_to_base(self):
        rtb = False
        rescan_time = time.time() + self.SEARCH_TIME
        while not rtb:
            print(self.high_rise)
            print(self.high_rise + self.zone_bound)
            find_target = self.Guidance.get_marker(self.robot, self.high_rise + self.zone_bound)
            print(find_target)
            if not find_target:
                return
            if find_target.id in self.high_rise: # if we found the highrise one
                print("FOUND HIGHRISE")
                dist, angle = self.Guidance.update_values(self.robot, find_target)  # get starting positions
                print(angle, dist)
                self.start_guidance(angle, dist, find_target)
            elif find_target in self.zone_bound:
                print("FOUND ZONE")
            else:
                pass

            if time.time() >= rescan_time:
                print("No Target Found, Moving to search")
                self.Motion.right(self.wheelMotor, 0.5)
                time.sleep(0.2)
                self.Motion.stop_motors(self.wheelMotor)
                rescan_time = time.time() + self.SEARCH_TIME


    def __call__(self, *args, **kwargs):
        self.InteractionSuite.arm_down()
        self.InteractionSuite.deactivate_solenoid()
        self.InteractionSuite.suck_solenoid_deactiv()

        print("HARDWARE READY")
        print("WAITING FOR START")

        self.robot.wait_start()
        self.InteractionSuite.main_arm_up(self.armPumpMotor, self.arduino)
        time.sleep(0.2)
        self.lock_target()


robo = RobotHandler()
robo()
