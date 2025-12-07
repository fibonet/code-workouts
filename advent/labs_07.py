#!/usr/bin/env python3
from collections import defaultdict


def count_active_splitters(manifold: list):
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


def quantum_count(manifold: list):
    beams = {manifold[0].index("S"): 1}

    for i, line in enumerate(manifold[1:]):
        next_gen = defaultdict(int)
        for pos, times in beams.items():
            if line[pos] == "^":
                next_gen[pos - 1] += times
                next_gen[pos + 1] += times
            else:
                manifold[i + 1][pos] = "|"
                next_gen[pos] += times

        beams = dict(next_gen.items())
        print(" ".join(line), "//", " ".join(map(str, beams.values())))


    return sum(beams.values())


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    manifold = list(map(list, content.split("\n")))

    splits = count_active_splitters(manifold)
    timelines = quantum_count(manifold)

    print(f"{splits=} and {timelines=}")


if __name__ == "__main__":
    main("07-easy.txt")
