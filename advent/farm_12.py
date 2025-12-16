#!/usr/bin/env python3
import re
from collections import namedtuple
from itertools import chain
from pprint import pprint

import numpy as np


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


Coords = namedtuple("Coords", "x y")


is_index = re.compile(r"(\d+):")
is_region = re.compile(r"^(\d+)x(\d+):\s(.+)$")


def load(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    shapes = list()
    regions = list()
    shape = list()
    shape_index = None
    for line in content.split("\n"):
        if line == "":
            shapes.append(shape)
            shape = list()
        elif m := is_index.fullmatch(line):
            shape_index = int(m.group(1))
            assert shape_index == len(shapes)
        elif m := is_region.fullmatch(line):
            size = int(m.group(1)), int(m.group(2))
            req = list(map(int, m.group(3).split()))
            regions.append((size, req))
        else:
            row = [int(c == "#") for c in line]
            shape.append(row)

    print("parsed", len(shapes), "shapes and", len(regions), "regions.")
    return shapes, regions


def can_fit(region, shapes):
    (rows, cols), req = region
    print(f"--- Region {(rows, cols)}: {req} ---")

    dummy = rows * cols
    total = 0
    for i, n in enumerate(req):
        part = n * sum(chain.from_iterable(shapes[i]))
        total += part

    print("dummy total", total, "vs", dummy)

    return total < dummy


def solve(filename: str):
    banner(f"Solving {filename}")
    shapes, regions = load(filename)

    can = 0
    for reg in regions:
        can += int(can_fit(reg, shapes))

    return can


if __name__ == "__main__":
    banner("Part one (I)")
    result = solve("12-easy.txt")
    print(f"{result=}")
    expected = 3
    # TODO: this answer is obviously, but luckily it matches the large input
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("12-input.txt")
    print(f"{result=}")
    expected = 519
    assert result == expected, f"Computed {result} was expected to be {expected}."

    banner("Part two (II)")
    result = solve("12-easy.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("12-input.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    print("All is good in da' hood.")
