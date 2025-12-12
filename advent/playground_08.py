#!/usr/bin/env python3
import enum
from collections import defaultdict, namedtuple
from functools import reduce
from heapq import heappop, heappush
from itertools import combinations
from math import dist
from operator import mul
from pprint import pprint

Coords = namedtuple("Coords", "i x y z")


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            # largest size first
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

        return True

    def components(self):
        comps = defaultdict(set)
        for i, p in enumerate(self.parent):
            r = self.find(p)
            comps[r].add(i)

        return sorted(comps.values(), key=len, reverse=True)


def make_connections(junction_boxes: list[Coords], limit=10):
    distances = list()
    for left, right in combinations(junction_boxes, 2):
        heappush(distances, (dist(left, right), left, right))

    networks = UnionFind(len(junction_boxes))
    for _ in range(limit):
        _, a, b = heappop(distances)
        networks.union(a.i, b.i)

    return networks.components()

def fill_connections(junction_boxes: list[Coords]):
    distances = list()
    for left, right in combinations(junction_boxes, 2):
        heappush(distances, (dist(left, right), left, right))

    networks = UnionFind(len(junction_boxes))
    last_pair = tuple()
    while len(networks.components()) > 1:
        _, a, b = heappop(distances)
        networks.union(a.i, b.i)
        last_pair = (a, b)

    return networks.components(), last_pair


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    junction_boxes = [
        Coords(i, *map(int, line.split(",")))
        for i, line in enumerate(content.split("\n"))
    ]
    print("Found", len(junction_boxes), "coordinates")

    circuits = make_connections(junction_boxes, limit=10)

    print("Top networks:")
    for i, nodes in enumerate(circuits[:10]):
        print(i, nodes)
        print(*(junction_boxes[k] for k in nodes))

    top_length = list(map(len, circuits))
    result = reduce(mul, top_length[:3], 1)
    print(" * ".join(map(str, top_length[:3])), "=", result)

    circuits, last_pair = fill_connections(junction_boxes)
    print("The network:")
    for i, nodes in enumerate(circuits[:10]):
        print(i, nodes)
        print(*(junction_boxes[k] for k in nodes))

    print("Last connection:", last_pair, last_pair[0].x * last_pair[1].x)

if __name__ == "__main__":
    main("./08-input.txt")
