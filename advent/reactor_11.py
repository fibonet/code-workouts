#!/usr/bin/env python3
from collections import deque
from functools import lru_cache
from pprint import pprint
from typing import Iterable


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


def count_paths(graph: dict, start: str, stop: str):
    print(f"Searching for paths from {start} to {stop}.")
    counter = 0
    queue = deque([start])
    while queue:
        pos = queue.pop()
        if pos == stop:
            counter += 1
        else:
            for move in graph[pos]:
                queue.appendleft(move)
    return counter


def count_paths_through(graph: dict, start: str, stop: str, required: Iterable):
    print(f"Searching for paths from {start} to {stop}.")
    required = frozenset(required)

    @lru_cache
    def dfs(node: str, remaining: set):
        if node in remaining:
            remaining = remaining - {node}
        if node == stop:
            return int(not remaining)
        return sum(dfs(nn, remaining) for nn in graph[node])

    return dfs(start, required)


def solve(filename: str):
    banner(f"Solving {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    graph = dict()
    for line in content.split("\n"):
        key, *values = line.split()
        graph[key.rstrip(":")] = values

    paths = count_paths(graph, "you", "out")
    print("Found", paths, "paths.")

    return paths


def solve_again(filename: str):
    banner(f"Solving again {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    graph = dict()
    for line in content.split("\n"):
        key, *values = line.split()
        graph[key.rstrip(":")] = values

    paths = count_paths_through(graph, "svr", "out", {"dac", "fft"})
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
    result = solve_again("./11-easy-two.txt")
    print(f"{result=}")
    expected = 2
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve_again("11-input.txt")
    print(f"{result=:_}")
    expected = 479511112939968
    assert result == expected, f"Computed {result} was expected to be {expected}."

    print("All is good in da' hood.")
