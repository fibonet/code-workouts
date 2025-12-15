#!/usr/bin/env python3
from collections import deque
from pprint import pprint


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


def bfs(graph: dict, start: str, stop: stop):
    print(f"Searching for paths from {start} to {stop}.")
    paths = 0
    queue = deque([start])
    while queue:
        pos = queue.pop()
        if pos == stop:
            paths += 1
        else:
            for move in graph[pos]:
                queue.appendleft(move)

    return paths


def solve(filename: str):
    banner(f"Solving {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    graph = dict()
    for line in content.split("\n"):
        key, *values = line.split()
        graph[key.rstrip(":")] = values

    paths = bfs(graph, "you", "out")
    print("Found", paths, "paths.")

    return paths


if __name__ == "__main__":
    banner("Part one (I)")
    result = solve("11-easy.txt")
    print(f"{result=}")
    expected = 5
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("11-input.txt")
    print(f"{result=}")
    expected = 543
    assert result == expected, f"Computed {result} was expected to be {expected}."

    banner("Part two (II)")
    result = solve("11-easy.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("11-input.txt")
    print(f"{result=}")
    expected = 0
    assert result == expected, f"Computed {result} was expected to be {expected}."

    print("All is good in da' hood.")
