#!/usr/bin/env python3
from collections import namedtuple
from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


Coords = namedtuple("Coords", "x y")


def render(filename: str):
    ax = plt.gca()
    ax.set_aspect("equal", "box")
    ax.invert_yaxis()

    # red tiles
    xs, ys = zip((1, 1), (2, 4), (3, 9))
    print(xs)
    print(ys)
    plt.plot(xs, ys, color="red")

    plt.savefig(f"{filename}.png", dpi=600)
    plt.close()


def solve(filename: str):
    banner(f"Solving {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    render(filename)

    return 0


if __name__ == "__main__":
    banner("Part one (I)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("10-input.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    banner("Part two (II)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("10-input.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    print("All is good in da' hood.")
