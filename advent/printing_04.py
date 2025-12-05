#!/usr/bin/env python3


def neighbours_of(pos: tuple[int, int], size: tuple[int, int]) -> tuple:
    ALL_NEIGHBOURS = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    row, col = pos
    rows, cols = size
    return tuple(
        (row + dr, col + dc)
        for dr, dc in ALL_NEIGHBOURS
        if 0 <= (row + dr) < rows and 0 <= (col + dc) < cols
    )


def find_removable_rolls(grid: list):
    size = len(grid), len(grid[0])
    counter = 0

    for row, full_row in enumerate(grid):
        for col, value in enumerate(full_row):
            if value == "@":
                pos = row, col
                nearby_rolls = sum(
                    grid[ri][ci] in {"@", "x"} for ri, ci in neighbours_of(pos, size)
                )
                if nearby_rolls < 4:
                    grid[row][col] = "x"
                    counter += 1

    return counter


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    grid = list(map(list, content.split()))

    removed_count = 0
    while find_removable_rolls(grid):
        for row, full_row in enumerate(grid):
            for col, value in enumerate(full_row):
                if value == "x":
                    grid[row][col] = "."
                    removed_count += 1

    print(f"There were {removed_count=} rolls removed.")


if __name__ == "__main__":
    main("04-input.txt")
