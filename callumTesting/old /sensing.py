import math

from sr.robot3 import *

robot = Robot()
pBoard = robot.power_board
backmBoard = robot.motor_boards["SR0UCD"]
frontmBoard = robot.motor_boards["SR0TCE"]
led = robot.kch

pBoard.outputs.power_on() # turn on pBoard
pBoard.outputs[OUT_H0].is_enabled = True

def dist_sens():
    dist = 0
    markers = robot.camera.see()
    for marker in markers:
        dist = marker.position.distance

    if dist > 1500:
        led.leds[LED_B].colour = Colour.RED
    elif 200 <= dist <= 1500:
        led.leds[LED_B].colour = Colour.BLUE
    elif dist < 200:
        led.leds[LED_B].colour = Colour.GREEN
    else:
        pass # should be fine

def angle_sens():
    angle = 0
    markers = robot.camera.see()
    for marker in markers:
        angle =math.degrees(marker.position.horizontal_angle)
    if angle < -15:
        led.leds[LED_A].colour = Colour.BLUE
        led.leds[LED_B].colour = Colour.OFF
        led.leds[LED_C].colour = Colour.OFF
    elif angle > 15:
        led.leds[LED_C].colour = Colour.BLUE
        led.leds[LED_B].colour = Colour.OFF
        led.leds[LED_A].colour = Colour.OFF
    else:
        led.leds[LED_B].colour = Colour.RED
        led.leds[LED_C].colour = Colour.OFF
        led.leds[LED_A].colour = Colour.OFF




while True:
    angle_sens()
