# #!/usr/bin/env pybricks-micropython

from time import sleep

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

ev3 = EV3Brick()

motor_left = Motor(Port.D)
motor_right = Motor(Port.A)
motor_grab = Motor(Port.C)

color_left = ColorSensor(Port.S1)
color_right = ColorSensor(Port.S4)

# ----------------------------

motor_left.run(-70)
motor_right.run(70)

lowest_intensity_left: int = 100
highest_intensity_left: int = 0
lowest_intensity_right: int = 100
highest_intensity_right: int = 0

while True:
    left_intensity = color_left.reflection()
    right_intensity = color_right.reflection()

    if left_intensity < lowest_intensity_left:
        lowest_intensity_left = left_intensity
    if left_intensity > highest_intensity_left:
        highest_intensity_left = left_intensity
    if right_intensity < lowest_intensity_right:
        lowest_intensity_right = right_intensity
    if right_intensity > highest_intensity_right:
        highest_intensity_right = right_intensity

    print("Left: %d, Right: %d" % (left_intensity, right_intensity))
    print(
        "Lowest Left: %d, Highest Left: %d"
        % (lowest_intensity_left, highest_intensity_left)
    )
    print(
        "Lowest Right: %d, Highest Right: %d"
        % (lowest_intensity_right, highest_intensity_right)
    )
    print()

    sleep(0.1)
