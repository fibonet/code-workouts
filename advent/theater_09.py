#!/usr/bin/env python3
from collections import defaultdict, namedtuple
from collections.abc import Generator
from itertools import chain, combinations
from pprint import pprint

import matplotlib.pyplot as plt


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


Coords = namedtuple("Coords", "x y")
RED = "#"
GREEN = "X"


def area(left: Coords, right: Coords) -> int:
    return (abs(right.x - left.x) + 1) * (abs(right.y - left.y) + 1)


def find_largest_rectangle(red_tiles: list):
    all_pairs = combinations(red_tiles, 2)
    largest_pair = next(all_pairs)
    largest_area = area(*largest_pair)
    for a, b in all_pairs:
        new_area = area(a, b)
        if new_area > largest_area:
            largest_pair = (a, b)
            largest_area = new_area

    return largest_area


def solve_largest(filename: str):
    print("Solving for", filename)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    tiles = [Coords(*map(int, line.split(","))) for line in content.split("\n")]
    print("Parsed", len(tiles), "red tiles.")

    largest_area = find_largest_rectangle(tiles)

    return largest_area


def contour_walk(a: Coords, b: Coords) -> Generator[Coords]:
    left = min(a.x, b.x)
    right = max(a.x, b.x)
    top = min(a.y, b.y)
    bottom = max(a.y, b.y)

    for i in range(left, right + 1):
        yield Coords(i, top)

    for i in range(top, bottom + 1):
        yield Coords(right, i)

    for i in range(left, right + 1):
        yield Coords(i, bottom)

    for i in range(top, bottom + 1):
        yield Coords(left, i)


def find_largest_color(red_tiles: list[Coords], green_tiles: list[Coords]):
    all_pairs = combinations(red_tiles, 2)
    largest_pair = next(all_pairs)
    largest_area = area(*largest_pair)

    by_rows = defaultdict(list)
    for ti in chain(red_tiles, green_tiles):
        by_rows[ti.y].append(ti.x)

    by_cols = defaultdict(list)
    for ti in chain(red_tiles, green_tiles):
        by_cols[ti.x].append(ti.y)

    for a, b in all_pairs:
        is_inside = True
        for ti in contour_walk(a, b):
            left, right = min(by_rows[ti.y]), max(by_rows[ti.y])
            if ti.x < left or ti.x > right:
                is_inside = False
                print(ti, "not inside, by row")
                break

            top, bottom = min(by_cols[ti.x]), max(by_cols[ti.x])
            if ti.y < top or ti.y > bottom:
                is_inside = False
                print(ti, "not inside, by col")
                break

        if not is_inside:
            continue

        new_area = area(a, b)
        if new_area > largest_area:
            largest_pair = (a, b)
            largest_area = new_area

    print("largest", *largest_pair)

    return largest_area


def solve_colorized(filename: str):
    print("Solving colors for", filename)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    red_tiles = [Coords(*map(int, line.split(","))) for line in content.split("\n")]
    print("Parsed", len(red_tiles), "red tiles.")

    rows = max(ti.y for ti in red_tiles) + 3
    cols = max(ti.x for ti in red_tiles) + 3

    # scan rows
    red_tiles.sort(key=lambda ti: (ti.y, ti.x))
    green_tiles = list()
    last = red_tiles[0]
    horizontal = list()
    left, right = last.x, last.x
    for ti in red_tiles[1:]:
        if ti.y == last.y:
            for ci in range(last.x + 1, ti.x):
                green_tiles.append(Coords(ci, ti.y))
            left, right = min(ti.x, left), max(ti.x, right)
        else:
            horizontal.append((Coords(left, last.y), Coords(right, last.y)))
            left, right = ti.x, ti.x

        last = ti
    horizontal.append((Coords(left, last.y), Coords(right, last.y)))

    print("Horizontal")
    print(*horizontal, sep="\n")

    # scan columns
    red_tiles.sort(key=lambda ti: (ti.x, ti.y))
    last = red_tiles[0]
    vertical = list()
    top, bottom = last.y, last.y
    for ti in red_tiles[1:]:
        if ti.x == last.x:
            for ri in range(last.y + 1, ti.y):
                green_tiles.append(Coords(ti.x, ri))
            top, bottom = min(ti.y, top), max(ti.y, bottom)
        else:
            vertical.append((Coords(last.x, top), Coords(last.x, bottom)))
            top, bottom = ti.y, ti.y
        last = ti
    vertical.append((Coords(last.x, top), Coords(last.x, bottom)))

    print("Vertical")
    print(*vertical, sep="\n")

    largest_area = find_largest_color(red_tiles, green_tiles)

    # render contour
    xs, ys = zip(*green_tiles)
    plt.scatter(xs, ys, s=0.1, color="green")
    xs, ys = zip(*red_tiles)
    plt.scatter(xs, ys, s=1, color="red")
    plt.gca().set_aspect("equal", "box")
    plt.gca().invert_yaxis()
    plt.savefig(f"{filename}.png", dpi=600)
    plt.close()

    raise RuntimeError("stop")
    return largest_area


if __name__ == "__main__":
    banner("Part one")
    largest_area = solve_largest("09-easy.txt")
    print(f"{largest_area=}")
    assert largest_area == 50, "Failed the easy input"

    largest_area = solve_largest("09-input.txt")
    print(f"{largest_area=}")
    assert largest_area == 4763932976, "Failed the large input"

    banner("Part two")
    largest_area = solve_colorized("09-easy.txt")
    print(f"{largest_area=}")
    assert largest_area == 24, "Failed the easy input"

    largest_area = solve_colorized("09-input.txt")
    print(f"{largest_area=}")
    assert largest_area == 4763932976, "Failed the large input"
