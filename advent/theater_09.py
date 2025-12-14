#!/usr/bin/env python3
from collections import namedtuple
from itertools import combinations
from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numpy import test


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


def is_inside(
    point: Coords, red_tiles: set, vertical_edges: dict, horizontal_edges
) -> bool:
    if point in red_tiles:
        return True

    h_crosses = 0
    for ex, (top, bottom) in vertical_edges.items():
        if ex > point.x and top <= point.y < bottom:
            h_crosses += 1

    v_crosses = 0
    for ey, (left, right) in horizontal_edges.items():
        if ey > point.y and left <= point.x < right:
            v_crosses += 1

    return h_crosses % 2 == 1


def rectangle_inside_polygon(
    left, right, top, bottom, horizontal_edges, vertical_edges
):
    # check top and bottom rectangle edges against vertical polygon edges
    for ex, (etop, ebottom) in vertical_edges.items():
        if (left < ex < right) and (etop < top < ebottom or etop < bottom < ebottom):
            return False

    # check left and right rectangle edges against horizontal polygon edges
    for ey, (eleft, eright) in horizontal_edges.items():
        if (top < ey < bottom) and (eleft < left < eright or eleft < right < eright):
            return False

    return True


def find_largest_color(
    red_tiles: list[Coords], horizontal_edges: dict, vertical_edges: dict
):
    all_pairs = combinations(red_tiles, 2)
    largest_pair = next(all_pairs)
    largest_area = area(*largest_pair)

    tiles = set(red_tiles)

    for a, b in all_pairs:
        left, right = min(a.x, b.x), max(a.x, b.x)
        top, bottom = min(a.y, b.y), max(a.y, b.y)

        test_points = [
            Coords(left, top),
            Coords(right, top),
            Coords(left, bottom),
            Coords(right, bottom),
        ]

        is_contained = all(
            is_inside(pi, tiles, vertical_edges, horizontal_edges) for pi in test_points
        ) and rectangle_inside_polygon(
            left, right, top, bottom, horizontal_edges, vertical_edges
        )
        if is_contained:
            new_area = area(a, b)
            if new_area > largest_area:
                largest_pair = (a, b)
                largest_area = new_area

    print("largest", *largest_pair)
    return largest_area, largest_pair


def render_tiles(
    red_tiles: list[Coords],
    corners: tuple[Coords, Coords],
    horizontal_edges: dict,
    vertical_edges: dict,
    filename: str,
):
    ax = plt.gca()
    ax.set_aspect("equal", "box")
    ax.invert_yaxis()

    # red tiles
    xs, ys = zip(*red_tiles)
    plt.scatter(xs, ys, color="red", s=1)

    # horizontal edges (green)
    for y, (left, right) in horizontal_edges.items():
        plt.plot([left, right], [y, y], color="green", linewidth=0.2)

    # vertical edges (green)
    for x, (top, bottom) in vertical_edges.items():
        plt.plot([x, x], [top, bottom], color="green", linewidth=0.2)

    # largest rectangle (blue)
    left = min(corners[0].x, corners[1].x)
    right = max(corners[0].x, corners[1].x)
    bottom = min(corners[0].y, corners[1].y)
    top = max(corners[0].y, corners[1].y)
    width = right - left
    height = top - bottom
    rect = Rectangle(
        (left, bottom), width, height, fill=False, edgecolor="blue", linewidth=1
    )
    ax.add_patch(rect)

    plt.savefig(f"{filename}.png", dpi=600)
    plt.close()


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

    # scan columns
    vertical_edges = dict()
    red_tiles.sort(key=lambda ti: (ti.x, ti.y))
    last = red_tiles[0]
    for ti in red_tiles[1:]:
        if ti.x == last.x:
            vertical_edges[last.x] = (last.y, ti.y)
        last = ti

    print(len(vertical_edges), "vertical lines")

    largest_area, corners = find_largest_color(
        red_tiles, horizontal_edges, vertical_edges
    )

    render_tiles(red_tiles, corners, horizontal_edges, vertical_edges, filename)

    # raise RuntimeError("Stop")
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
    assert largest_area == 1501292304, "Failed the large input"

    print("All is good in da' hood.")
