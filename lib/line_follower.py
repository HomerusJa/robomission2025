from time import sleep

from pybricks.ev3devices import ColorSensor, Motor

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
        base_speed: int = 100,
        kp: float = 1.0,
        line_threshold: int = 15,
    ):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_color_sensor = left_color_sensor
        self.right_color_sensor = right_color_sensor

        self.base_speed = base_speed
        self.kp = kp
        self.line_threshold = line_threshold

    def _tick(self):
        """Follows the line for one time step."""
        left_intensity = self.left_color_sensor.reflection()
        right_intensity = self.right_color_sensor.reflection()

        # If diff is
        # - positive: left is brighter than right, so turn right
        # - negative: right is brighter than left, so turn left
        diff = left_intensity - right_intensity

        left_motor_speed = self.base_speed + self.kp * diff
        right_motor_speed = self.base_speed - self.kp * diff

        self.left_motor.run(left_motor_speed)
        self.right_motor.run(right_motor_speed)

    def _is_on_line(self):
        """Returns True if both sensors are on the line, indicating the robot is on a straight end."""
        return (
            self.left_color_sensor.reflection() < self.line_threshold
            and self.right_color_sensor.reflection() < self.line_threshold
        )

    def _stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def follow_line_for_seconds(self, duration_sec: int = 10):
        """Follows a line for a given duration in seconds."""

        for _ in range(duration_sec // SLEEP_INTERVAL):
            self._tick()
            sleep(SLEEP_INTERVAL)

        self._stop()

    def follow_line_until_crossing(self):
        """Follows a line until a crossing is detected."""
        while not self._is_on_line():
            self._tick()
            sleep(SLEEP_INTERVAL)

        self._stop()

    def straight_until_line(self):
        """Drives straight until a line is detected."""
        self.left_motor.run(self.base_speed)
        self.right_motor.run(self.base_speed)

        while not self._is_on_line():
            sleep(SLEEP_INTERVAL)

        self._stop()
