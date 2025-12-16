#!/usr/bin/env python3
import re
from collections import namedtuple
from pprint import pprint


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
            shape.append(line.replace("#", "1").replace(".", "0"))

    print("parsed", len(shapes), "shapes and", len(regions), "regions.")
    return shapes, regions


def solve(filename: str):
    banner(f"Solving {filename}")
    shapes, regions = load(filename)
    pprint(shapes)
    pprint(regions)

    return 0


if __name__ == "__main__":
    banner("Part one (I)")
    result = solve("12-easy.txt")
    print(f"{result=}")
    expected = 2
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("12-input.txt")
    print(f"{result=}")
    expected = 0
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
