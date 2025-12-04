#!/usr/bin/env python3


def count_zero_touches(lines: list[str], start=50, limit=100):
    position = start
    DIRECTIONS = dict(R=1, L=-1)

    counter = 0
    for move in lines:
        direction, steps = DIRECTIONS[move[0]], int(move[1:])

        extra, remaining = divmod(steps, limit)
        counter += extra
        last_position, position = position, position + direction * remaining

        if (position <= 0 or position >= limit) and last_position != 0:
            counter += 1

        print(
            f"{direction:2}x{steps:2}: {position:3} [{position % limit:3}], #{counter}"
        )
        position %= limit

    return counter


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read()
        lines = content.strip().split("\n")
        print("read", len(lines), "lines from", filename)

    zeros = count_zero_touches(lines)
    print(filename, "moves went through zero", zeros, "times.")


if __name__ == "__main__":
    main("01-input.txt")
