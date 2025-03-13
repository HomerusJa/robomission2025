from pybricks.ev3devices import Motor
from pybricks.parameters import Stop


class Grappler:
    def __init__(self, motor: Motor, closed_angle: int = -90):
        """Initialize the Grappler object.

        To initialize the position of the motor, run Grappler.initialize().

        Args:
            motor (Motor): The motor that controls the grappler.
            closed_angle (int, optional): The angle at which the grappler is
                closed. Defaults to -90 deg. Note that this angle is the angle
                from the upper position of the motor.
        """
        self.motor = motor
        self.closed_angle = closed_angle

    async def initialize(self, speed: int = 500):
        """Initializes the grappler by moving the motor to a known location and
        resetting the angle. This way we always know a rather precisely the
        motors position.

        Args:
            speed (int, optional): The speed at which the motor should move. Defaults to 500 deg/s.
        """
        # TODO: Maybe use Stop.BRAKE instead of Stop.HOLD
        stop_angle = await self.motor.run_until_stalled(speed=speed, then=Stop.HOLD)
        print(f"Resetting the motor angle from {stop_angle=} to 0.")
        self.motor.reset_angle(0)

    async def grab(self, speed: int = 500) -> None:
        """Move the motor to a position where the grappler is closed."""
        await self.motor.run_target(speed, self.closed_angle)

    async def release(self, speed: int = 500) -> None:
        """Move the motor to a position where the grappler is open."""
        # FIXME: Maybe don't fully open, also, this overlaps with the initialize method
        await self.motor.run_target(speed, 0)
