import cmath
import math
import sys
from functools import partial

SIZE = complex(7000, 3000)
MARS_GRAVITY = 3.711
MAX_THRUST = 4
MAX_FLY_TILT = 45
MAX_LAND_TILT = 9


def lerp(x, x1, x2, y1, y2):
    clamp_x = max(x1, min(x, x2))
    norm_x = (clamp_x - x1) / (x2 - x1) if (x2 - x1) != 0 else 0
    return y1 + (y2 - y1) * norm_x


lerp_thrust = partial(lerp, x1=0, x2=13, y1=0, y2=4)


def clamp(left, x, right):
    return max(left, min(x, right))


def log_distance(x: int, left: int, right: int, damp=16):
    if left < x < right:
        return 0
    if x < left:
        distance = x - left
    else:
        distance = x - right
    return math.copysign(math.log(abs(distance) / damp + 1), distance)


def flight_control(position, velocity, target):
    kp_pos = 0.0025
    kp_velo = 0.5
    target_velocity = complex(0, 0)

    pos_err = target - position
    velo_err = target_velocity - velocity
    control_cc = kp_pos * pos_err + kp_velo * velo_err

    power, direction = cmath.polar(control_cc)
    if direction <= 0:
        max_tilt = MAX_FLY_TILT
        as_tilt = -direction - cmath.pi / 2
        thrust = 4 - int(lerp_thrust(abs(control_cc.imag)))
    else:
        # should go up
        max_tilt = MAX_FLY_TILT  # MAX_LAND_TILT
        as_tilt = direction - cmath.pi / 2
        thrust = 4
    print(
        f"{math.degrees(direction):.0f} vs {math.degrees(as_tilt):.0f} <)",
        file=sys.stderr,
    )
    print(
        f"{control_cc:.1f} / {power:.1f} ~ {lerp_thrust(power):.1f}",
        file=sys.stderr,
    )

    tilt = min(max_tilt, max(-max_tilt, int(math.degrees(as_tilt))))

    return tilt, thrust


def landing_control(position, velocity, target):
    kp_pos = 0.004
    kp_velo = 0.5
    target_velocity = complex(0, -38)

    pos_err = target - position
    velo_err = target_velocity - velocity
    control_cc = kp_pos * pos_err + kp_velo * velo_err

    power, direction = cmath.polar(control_cc)
    if direction <= 0:
        as_tilt = -direction - cmath.pi / 2
        thrust = 4 - int(lerp_thrust(abs(control_cc.imag)))
    else:
        as_tilt = direction - cmath.pi / 2
        thrust = 4
    print(
        f"{math.degrees(direction):.0f} vs {math.degrees(as_tilt):.0f} <)",
        file=sys.stderr,
    )
    print(
        f"{control_cc:.1f} / {power:.1f} ~ {lerp_thrust(power):.1f}",
        file=sys.stderr,
    )

    if abs(pos_err.imag) < 100:
        tilt = 0
    else:
        tilt = min(MAX_LAND_TILT, max(-MAX_LAND_TILT, int(math.degrees(as_tilt))))

    return tilt, thrust


## Parse landscape
land_points = int(input())
landscape = list()
previous = complex()
target = complex()
platform_width = 0
for i in range(land_points):
    pt = complex(*(int(j) for j in input().split()))
    landscape.append(pt)
    if pt.imag == previous.imag:
        target = complex((previous.real + pt.real) / 2, pt.imag)
        platform_width = (pt.real - previous.real) / 2
    previous = pt

is_landing = False
start_y = None
high_target = complex()
while True:
    x, y, hs, vs, fuel, tilt, thrust = [int(i) for i in input().split()]
    pos = complex(x, y)
    velocity = complex(hs, vs)
    if start_y is None:
        start_y = y
        high_target = complex(target.real, start_y - 100)

    print(is_landing, pos, velocity, fuel, tilt, thrust, file=sys.stderr)
    if is_landing:
        tilt, thrust = landing_control(pos, velocity, target)
    else:
        tilt, thrust = flight_control(pos, velocity, high_target)
        if abs(target.real - x) < platform_width and abs(hs) < 9:
            is_landing = True

    print(tilt, thrust)
