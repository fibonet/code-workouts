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


def find_largest_color(
    red_tiles: list[Coords], horizontal_edges: dict, vertical_edges: dict
):
    all_pairs = combinations(red_tiles, 2)
    largest_pair = next(all_pairs)
    largest_area = area(*largest_pair)

    tiles = set(red_tiles)

    for a, b in all_pairs:
        print("working on", (a, b))
        # a, b are definitely inside, so the question is where do the other corners are
        c1 = Coords(a.x, b.y)
        print("Corner", c1)
        if c1 in tiles:
            c1_is_inside = True
            print("c1 is a red tile")
        else:
            h_cross = False
            for ey, (left, right) in horizontal_edges.items():
                if left <= c1.x <= right:
                    h_cross = not h_cross
                    print("h cross", ey, (left, right))

            v_cross = False
            for ex, (top, bottom) in vertical_edges.items():
                if top < c1.y < bottom:
                    v_cross = not v_cross
                    print("v cross", ex, (top, bottom))

            c1_is_inside = h_cross and v_cross
            if c1_is_inside:
                print("c1 is inside", h_cross, v_cross)
            else:
                print("c1 is outside", h_cross, v_cross)

        c2 = Coords(b.x, a.y)
        print("Corner", c2)
        if c2 in tiles:
            c2_is_inside = True
            print("c2 is a red tile")
        else:
            h_cross = False
            for ey, (left, right) in horizontal_edges.items():
                if left < c2.x < right:
                    h_cross = not h_cross

            v_cross = False
            for ex, (top, bottom) in vertical_edges.items():
                if top < c2.y < bottom:
                    v_cross = not v_cross

            c2_is_inside = h_cross and v_cross
            if c2_is_inside:
                print("c2 is inside", h_cross, v_cross)
            else:
                print("c2 is outside", h_cross, v_cross)

        if not c1_is_inside or not c2_is_inside:
            continue

        new_area = area(a, b)
        if new_area > largest_area:
            largest_pair = (a, b)
            largest_area = new_area

    print("largest", *largest_pair)

    raise RuntimeError("Stop")
    return largest_area, largest_pair


def solve_colorized(filename: str):
    print("Solving colors for", filename)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    red_tiles = [Coords(*map(int, line.split(","))) for line in content.split("\n")]
    print("Parsed", len(red_tiles), "red tiles.")

    # scan rows
    horizontal_edges = dict()
    red_tiles.sort(key=lambda ti: (ti.y, ti.x))
    last = red_tiles[0]
    for ti in red_tiles[1:]:
        if ti.y == last.y:
            horizontal_edges[last.y] = (last.x, ti.x)
        last = ti

    print(len(horizontal_edges), "horizontal lines")
    pprint(horizontal_edges)

    # scan columns
    vertical_edges = dict()
    red_tiles.sort(key=lambda ti: (ti.x, ti.y))
    last = red_tiles[0]
    for ti in red_tiles[1:]:
        if ti.x == last.x:
            vertical_edges[last.x] = (last.y, ti.y)
        last = ti

    print(len(vertical_edges), "vertical lines")
    pprint(vertical_edges)

    largest_area, corners = find_largest_color(
        red_tiles, horizontal_edges, vertical_edges
    )

    # render contour
    plt.gca().set_aspect("equal", "box")
    plt.gca().invert_yaxis()

    xs, ys = zip(*red_tiles)
    plt.scatter(xs, ys, s=1, color="red")

    left = min(corners[0].x, corners[1].x)
    right = max(corners[0].x, corners[1].x)
    bottom = min(corners[0].y, corners[1].y)
    top = max(corners[0].y, corners[1].y)

    width = right - left
    height = top - bottom

    from matplotlib.patches import Rectangle

    ax = plt.gca()

    rect = Rectangle(
        (left, bottom), width, height, fill=False, edgecolor="blue", linewidth=1
    )

    ax.add_patch(rect)

    plt.savefig(f"{filename}.png", dpi=600)
    plt.close()

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
