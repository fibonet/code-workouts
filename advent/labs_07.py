#!/usr/bin/env python3
from collections import deque
from operator import itemgetter


def simulation(manifold: list):
    splits = 0
    timelines = 1
    beams = {manifold[0].index("S")}

    for i, line in enumerate(manifold[1:]):
        to_do = set()
        for beam in beams:
            if line[beam] == "^":
                splits += 1
                to_do.add(("stop", beam))
                to_do.add(("start", beam - 1))
                to_do.add(("start", beam + 1))
            else:
                manifold[i + 1][beam] = "|"

        for act, pos in to_do:
            if act == "stop":
                beams.remove(pos)
            elif act == "start":
                beams.add(pos)

        print(" ".join(line), f"{splits} / {timelines}")

    return splits


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    manifold = list(map(list, content.split("\n")))

    splits = simulation(manifold)

    print(f"{splits=}")


if __name__ == "__main__":
    main("07-easy.txt")
