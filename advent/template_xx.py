#!/usr/bin/env python3
from collections import namedtuple
from itertools import combinations
from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


Coords = namedtuple("Coords", "x y")


def render_tiles(filename: str):
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

    render_tiles(filename)

    return 0


if __name__ == "__main__":
    banner("Part one (I)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    assert result == 0, "Failed the easy input"

    result = solve("10-input.txt")
    print(f"{result=}")
    assert result == 0, "Failed the large input"

    banner("Part two (II)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    assert result == 0, "Failed the easy input"

    result = solve("10-input.txt")
    print(f"{result=}")
    assert result == 0, "Failed the large input"

    print("All is good in da' hood.")
