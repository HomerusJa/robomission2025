# #!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import run_task

from lib.grappler import Grappler
from lib.line_follower import LineFollower

ev3 = EV3Brick()

motor_left = Motor(Port.D)
motor_right = Motor(Port.A)

# TODO: Check these ports
motor_grab = Motor(Port.C, gears=None)  # TODO: Add gears
motor_ball = Motor(Port.B)

color_left = ColorSensor(Port.S1)
color_right = ColorSensor(Port.S4)

drive_base = DriveBase(motor_left, motor_right, wheel_diameter=62.4, axle_track=21.1)
line_follower = LineFollower(
    motor_left, motor_right, color_left, color_right, drive_base
)
grappler = Grappler(motor_grab, closed_angle=-90)  # TODO: Check closed angle value
ball_grabber = Grappler(motor_ball, closed_angle=-90)  # TODO: Check closed angle value

# -----------------------------------------------------------------------------


def main():
    ev3.speaker.beep()

    line_follower.straight_until_line()
    drive_base.turn(90)
    line_follower.follow_line_until_crossing()
    drive_base.turn(-90)
    # TODO: Check distance
    line_follower.follow_line_for_distance(500, backwards=True)
    # ...


if __name__ == "__main__":
    main()
