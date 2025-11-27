import sys
from dataclasses import dataclass

SIZE = complex(7000, 3000)
MARS_GRAVITY = 3.711
MAX_THRUST = 4
MAX_FLY_TILT = 45
MAX_LAND_TILT = 9
GLIDE_HEIGHT = 2700


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


@dataclass
class PidController:
    setpoint: float
    kp: float
    ki: float
    kd: float

    integral: float = 0
    error: float = 0

    def __str__(self):
        return f"e: {self.error:.3}, i: {self.integral:.3}"

    def output(self, actual):
        distance = self.setpoint - actual
        proportional = distance * self.kp
        integral = (self.integral + distance) * self.ki
        derivative = (distance - self.error) * self.kd

        # Save state for next invokation
        self.integral = integral
        self.error = distance

        log(
            f"d: {distance} / p:{proportional:.3} + i:{integral:.3} + d:{derivative:.3}"
        )

        out = proportional + integral + derivative
        log(out, "=>", int(out))

        return int(out)


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

thruster = PidController(target.imag, kp=1 / 100, ki=1 / 1000, kd=1 / 100)
tilter = PidController(target.real, kp=1 / 50, ki=1 / 1000, kd=1)

# run once to eliminate the huge error on first step
x, y, hs, vs, fuel, tilt, thrust = tuple(map(int, input().split()))
position = complex(x, y)
velocity = complex(hs, vs)
tilt = tilter.output(position.real)
h_distance = target.real - position.real
print(45 if h_distance < 0 else -45, 4)

while True:
    x, y, hs, vs, fuel, tilt, thrust = tuple(map(int, input().split()))

    position = complex(x, y)
    velocity = complex(hs, vs)
    h_distance = target.real - position.real

    tilt = tilter.output(position.real)

    if abs(h_distance) < target_width / 2:
        # go into descent mode
        what = thruster.output(position.imag)
        thrust_f = linear_interpolation(-50, 0, 0, 4, what)
        log("thr", thrust_f)
        thrust = int(thrust_f)
    else:
        thrust = 4

    print(-tilt, thrust)
