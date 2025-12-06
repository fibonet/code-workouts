#!/usr/bin/env python3
from collections import defaultdict, deque
from functools import reduce
from operator import add, mul

OPS = {
    "+": (add, 0),
    "*": (mul, 1),
}


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    grid = list()
    operators = list()

    for line in iter(content.split("\n")):
        if line[0] not in {"+", "*"}:
            grid.append(list(line + " "))
        else:
            operators.extend(line.split())

    print(*grid, sep="\n")
    print("ops", operators)
    total = 0

    rows = len(grid)
    columns = len(grid[0])
    values = list()
    index = 0
    for col in range(columns):
        digits = [digit for row in range(rows) if (digit := grid[row][col]) != " "]
        if digits:
            value = int("".join(digits))
            values.append(value)
        else:
            op, initial = OPS[operators[index]]
            result = reduce(op, values, initial)
            print(values, op, result, initial)
            total += result
            index += 1
            values = list()

    print("The whole thing adds up to", total)


if __name__ == "__main__":
    main("./06-input.txt")
