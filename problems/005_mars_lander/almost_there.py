import math
import sys

MAX_THRUST = 4.0
MAX_TILT = 24
MAX_SPEED = 100
MAX_LANDING_SPEED = 15
MAX_DESCENT_SPEED = 32
GRAVITY = 3.711
MASS = MAX_THRUST / GRAVITY
GLIDE_ALT = 2700
SIZE_WIDTH = 7000
SIZE_HEIGHT = 3000


def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def linear_interpolation(x1, x2, y1, y2, x):
    """
    Compute the linear interpolation for a given x
    between points (x1, y1) and (x2, y2).
    """
    if x2 == x1:
        raise ValueError("x1 and x2 cannot be the same value.")

    y = y1 + ((x - x1) * (y2 - y1) / (x2 - x1))
    return y


def clamp(value: float, ref: tuple[float, float]):
    return max(min(value, ref[1]), ref[0])


class PidController:
    def __init__(self, kp: float, ki: float, kd: float, imax=5.0):
        self.target = None
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.imax = imax
        self.previous_error = 0.0

    def __str__(self):
        return f"err:{self.previous_error:.3f} -> {self.target:.3f}"

    def setpoint(self, target: float):
        self.target = target

    def update(self, actual):
        error = self.target - actual

        self.integral += error
        if abs(self.integral) > self.imax:
            self.integral = math.copysign(self.imax, self.integral)

        derivative = error - self.previous_error
        self.previous_error = error

        control = self.kp * error + self.ki * self.integral + self.kd * derivative
        log(
            "..",
            f"p:{self.kp * error:.3f}",
            f"i:{self.ki * self.integral:.3f}",
            f"d:{self.kd * derivative:.3f}",
            "..",
        )
        return control


# NOTE: Parse terrain
terrain = list()
target = complex()
target_width = 1
previous = complex()

size = int(input())
for i in range(size):
    coords = tuple(map(int, input().split()))
    current = complex(*coords)
    terrain.append(current)

    # landing target is in the middle of straigh section
    if current.imag == previous.imag:
        target = (previous + current) / 2
        target_width = abs(current - previous)

    previous = current

lateral_position = PidController(kp=1 / 40, ki=1 / 50, kd=1 / 25, imax=MAX_SPEED)
lateral_control = PidController(kp=1 / 10, ki=1 / 50, kd=1 / 25, imax=GRAVITY)
altitude = PidController(kp=1 / 40, ki=1 / 50, kd=1 / 20, imax=MAX_SPEED)
descent = PidController(kp=1 / 10, ki=1 / 20, kd=1 / 20, imax=MAX_SPEED)

lateral_position.setpoint(target.real)
altitude.setpoint(GLIDE_ALT)
tilt_limiter = MAX_TILT

while True:
    x, y, hs, vs, fuel, tilt, thrust = tuple(map(int, input().split()))

    position = complex(x, y)
    velocity = complex(hs, vs)
    distance = target - position
    h_distance = target.real - position.real

    desired_velocity = lateral_position.update(position.real)
    log(f"{desired_velocity=:.4f}", lateral_position)

    if abs(h_distance) < 750:
        velocity_ref = clamp(desired_velocity, (-MAX_LANDING_SPEED, +MAX_LANDING_SPEED))
    else:
        velocity_ref = clamp(desired_velocity, (-MAX_SPEED, +MAX_SPEED))
    lateral_control.setpoint(velocity_ref)

    desired_acc = lateral_control.update(velocity.real)
    log(f"{desired_acc=:.4f}", lateral_control)
    acc_ref = clamp(desired_acc, (-GRAVITY, +GRAVITY))

    theta_ref = math.asin(acc_ref / GRAVITY)
    theta_deg = math.degrees(theta_ref)
    log(f"tilt angle: {theta_ref:.4f} > {theta_deg:.0f}°")

    if abs(h_distance) < (target_width / 2) and abs(velocity.real) < MAX_LANDING_SPEED:
        altitude.setpoint(target.imag)
        v_distance = target.imag - position.imag
    else:
        v_distance = GLIDE_ALT - position.imag

    if abs(distance) < 300:
        tilt_limiter = 0

    desired_vert_speed = altitude.update(position.imag)
    log(f"{desired_vert_speed=:.4f}", altitude)

    descent_ref = clamp(desired_vert_speed, (-MAX_DESCENT_SPEED, 0))
    descent.setpoint(descent_ref)
    desired_descent = descent.update(velocity.imag)
    descent_acc = clamp(desired_descent, (-MAX_THRUST, 0))
    log(f"{desired_descent=:.4f} vs {descent_acc}", descent)

    ###
    thrust = int(MAX_THRUST + descent_acc)
    tilt = int(clamp(theta_deg, (-tilt_limiter, +tilt_limiter)))

    print(-tilt, thrust)
