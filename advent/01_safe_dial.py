#!/usr/bin/env python3


def playback(lines: list[str], start=50, limit=100):
    pos = start
    DIRECTIONS = dict(R=1, L=-1)

    counter = 0
    for move in lines:
        direction, steps = DIRECTIONS[move[0]], int(move[1:])
        pos += direction * steps
        pos %= limit
        if pos == 0:
            counter += 1

    return counter


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read()
        lines = content.strip().split("\n")
        print("read", len(lines), "lines from", filename)

    zeros = playback(lines)
    print(filename, "moves went through zero", zeros, "times.")

if __name__ == "__main__":
    main("01-input.txt")
