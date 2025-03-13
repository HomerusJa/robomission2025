from time import sleep
from typing import Tuple, Union

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.robotics import DriveBase

SLEEP_INTERVAL = 0.03

SLOW_SPEED = 50
FAST_SPEED = 100


class LineFollower:
    def __init__(
        self,
        left_motor: Motor,
        right_motor: Motor,
        left_color_sensor: ColorSensor,
        right_color_sensor: ColorSensor,
        drive_base: Union[DriveBase, None] = None,
        base_speed: int = 100,
        kp: float = 1.0,
        line_threshold: int = 15,
    ):
        """Initializes the LineFollower object."""
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor
        self.drive_base = drive_base

        self.base_speed = base_speed
        self.kp = kp
        self.line_threshold = line_threshold

    def _tick(self, backwards: bool) -> Tuple[int, int]:
        """Follows the line for one time step.

        Args:
            backwards (bool): If True, the robot drives backwards.

        Returns:
            Tuple[int, int]: The motor speeds for the left and right motor.
        """
        left_intensity = self.left_color_sensor.reflection()
        right_intensity = self.right_color_sensor.reflection()

        # If diff is
        # - positive: left is brighter than right, so turn right
        # - negative: right is brighter than left, so turn left
        diff = left_intensity - right_intensity

        backwards_factor = -1 if backwards else 1
        left_motor_speed = backwards_factor * self.base_speed + self.kp * diff
        right_motor_speed = backwards_factor * self.base_speed - self.kp * diff

        self.left_motor.run(left_motor_speed)
        self.right_motor.run(right_motor_speed)

        return left_motor_speed, right_motor_speed

    def _is_on_line(self):
        """Returns True if both sensors are on the line, indicating the robot is on a straight end."""
        return (
            self.left_color_sensor.reflection() < self.line_threshold
            and self.right_color_sensor.reflection() < self.line_threshold
        )

    def _stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def follow_line_for_seconds(self, duration_sec: int = 10, backwards: bool = False):
        """Follows a line for a given duration in seconds."""

        for _ in range(duration_sec // SLEEP_INTERVAL):
            self._tick(backwards)
            sleep(SLEEP_INTERVAL)

        self._stop()

    def follow_line_until_crossing(self, backwards: bool = False):
        """Follows a line until a crossing is detected."""
        while not self._is_on_line():
            self._tick(backwards)
            sleep(SLEEP_INTERVAL)

        self._stop()

    def follow_line_for_angle(self, angle_deg: int, backwards: bool = False):
        """Follows a line until the two motors have turned a given angle on average.

        Args:
            angle (int): The angle to turn in degrees. Should be positive (but itsdxy works with negative angles too).
            backwards (bool): If True, the robot drives backwards.
        """
        right_start_angle = self.right_motor.angle()
        left_start_angle = self.left_motor.angle()
        # Normalize the angle to be negative when driving backwards and positive otherwise
        cleaned_angle = -abs(angle_deg) if backwards else abs(angle_deg)

        while (
            self.right_motor.angle()
            - right_start_angle
            + self.left_motor.angle()
            - left_start_angle
        ) / 2 < cleaned_angle:
            self._tick(backwards)
            sleep(SLEEP_INTERVAL)

        self._stop()

    def follow_line_for_distance(self, distance_mm: int, backwards: bool = False):
        """Follow a line for a given distance."""
        start_distance = self.drive_base.distance()

        while abs(self.drive_base.distance() - start_distance) < distance_mm:
            self._tick(backwards)
            sleep(SLEEP_INTERVAL)

        self._stop()

    def straight_until_line(self, backwards: bool = False):
        """Drives straight until a line is detected."""
        self.left_motor.run(-self.base_speed if backwards else self.base_speed)
        self.right_motor.run(-self.base_speed if backwards else self.base_speed)

        while not self._is_on_line():
            sleep(SLEEP_INTERVAL)

        self._stop()
