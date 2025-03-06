# #!/usr/bin/env pybricks-micropython

from time import sleep

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port


def main():
    ev3 = EV3Brick()

    motor_grab = Motor(Port.C)

    def run_motor_for_seconds(motor: Motor, speed: int, seconds: float):
        motor.run(speed)
        sleep(seconds)
        motor.stop()

    ev3.speaker.beep()

    print("Starting")
    run_motor_for_seconds(motor_grab, 100, 5)
    print("Grabbed")
    run_motor_for_seconds(motor_grab, -100, 5)
    print("Released")
