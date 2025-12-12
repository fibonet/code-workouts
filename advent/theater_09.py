#!/usr/bin/env python3
from collections import namedtuple
from itertools import combinations
from operator import attrgetter


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


def find_largest_color(red_tiles: list[Coords], grid: list[list[str]]):
    all_pairs = combinations(red_tiles, 2)
    largest_pair = next(all_pairs)
    largest_area = area(*largest_pair)
    for a, b in all_pairs:
        if (
            any(grid[a.y][ci] == "." for ci in range(a.x + 1, b.x))
            or any(grid[b.y][ci] == "." for ci in range(a.x + 1, b.x))
            or any(grid[ri][a.x] == "." for ri in range(a.y + 1, b.y))
            or any(grid[ri][b.x] == "." for ri in range(a.y + 1, b.y))
        ):
            # check if all tiles on countour are empty
            continue

        new_area = area(a, b)
        if new_area > largest_area:
            largest_pair = (a, b)
            largest_area = new_area

    return largest_area


def solve_colorized(filename: str):
    print("Solving colors for", filename)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    tiles = [Coords(*map(int, line.split(","))) for line in content.split("\n")]
    print("Parsed", len(tiles), "red tiles.")

    rows = max(ti.y for ti in tiles) + 3
    cols = max(ti.x for ti in tiles) + 3
    print("Grid size", rows, "x", cols)

    if max(rows, cols) > 10000:
        raise ValueError(f"Grid of {rows:_} x {cols:_} = {rows * cols:_} is too big.")

    grid = [["."] * cols for _ in range(rows)]

    # scan rows
    tiles.sort(key=lambda ti: (ti.y, ti.x))
    contour = tiles.copy()
    last = tiles[0]
    for ti in tiles[1:]:
        if ti.y == last.y:
            for ci in range(last.x + 1, ti.x):
                contour.append(Coords(ci, ti.y))
        last = ti

    # scan columns
    tiles.sort(key=lambda ti: (ti.x, ti.y))
    last = tiles[0]
    for ti in tiles[1:]:
        if ti.x == last.x:
            for ri in range(last.y + 1, ti.y):
                contour.append(Coords(ti.x, ri))
        last = ti

    print(*contour, sep="\n")
    largest_area = find_largest_color(tiles, grid)

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
