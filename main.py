# #!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task

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

# TODO: Verify axle_track
drive_base = DriveBase(motor_left, motor_right, wheel_diameter=62.4, axle_track=21.1)
line_follower = LineFollower(
    motor_left, motor_right, color_left, color_right, drive_base
)
grappler = Grappler(motor_grab, closed_angle=-90)  # TODO: Check closed angle value
ball_grabber = Grappler(motor_ball, closed_angle=-90)  # TODO: Check closed angle value

# -----------------------------------------------------------------------------


async def mission() -> None:
    await line_follower.straight_until_line()
    await drive_base.turn(90)
    await line_follower.follow_line_until_crossing()
    await drive_base.turn(-90)
    # TODO: Check distance
    await line_follower.follow_line_for_distance(500, backwards=True)
    # ...


async def main():
    ev3.speaker.beep()
    multitask(grappler.initialize(), ball_grabber.initialize(), mission())


if __name__ == "__main__":
    run_task(main())
