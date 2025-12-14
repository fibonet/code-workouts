#!/usr/bin/env python3
from collections import deque
from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Tuple


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


@dataclass
class Machine:
    goal: int = 0
    size: int = 0
    specs: str = ""
    start: int = 0
    buttons: List = field(default_factory=list)
    joltage: Tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for token in self.specs.split():
            if token.startswith("["):
                values = token.strip("[]")[::-1]
                self.goal = int(values.replace("#", "1").replace(".", "0"), 2)
                self.size = len(values)
            elif token.startswith("("):
                values = token.strip("()")
                self.buttons.append(
                    sum(1 << pos for pos in map(int, values.split(",")))
                )
            elif token.startswith("{"):
                self.joltage += tuple(map(int, token.strip("{}").split(",")))

    def __str__(self) -> str:
        buttons = ", ".join(map(lambda tu: format(tu, "b"), self.buttons))
        lights = f"{self.goal:0{self.size}b}"
        return f"Buttons: ( {buttons} )\nGoal: [ {lights} ]"

    def solve_lights(self):
        trail = {self.start: (None, None)}

        queue = deque()
        state = self.start

        while state != self.goal:
            for bi in self.buttons:
                next_state = state ^ bi
                if next_state == state or next_state in trail:
                    continue
                else:
                    trail[next_state] = (state, bi)
                    queue.appendleft(next_state)

            state = queue.pop()
            # print(f"-> {state:0{self.size}b}, {queue}")

        solution = deque()
        state, btn = trail[state]
        while btn:
            solution.appendleft(btn)
            state, btn = trail[state]

        return solution

    def solve_joltage(self):
        trail = {self.start: (None, None)}

        queue = deque()
        state = self.start

        while state != self.goal:
            for bi in self.buttons:
                next_state = state ^ bi
                if next_state == state or next_state in trail:
                    continue
                else:
                    trail[next_state] = (state, bi)
                    queue.appendleft(next_state)

            state = queue.pop()
            # print(f"-> {state:0{self.size}b}, {queue}")

        solution = deque()
        state, btn = trail[state]
        while btn:
            solution.appendleft(btn)
            state, btn = trail[state]

        return solution

def solve(filename: str):
    banner(f"Solving {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    machines = [Machine(specs=line) for line in content.split("\n")]

    count = 0
    for machine in machines:
        push_log = machine.solve_lights()
        pretty_log = " > ".join(format(i, "b") for i in push_log)
        print(machine)
        print("push_log", pretty_log)
        count += len(push_log)

    return count


if __name__ == "__main__":
    banner("Started Part one (I)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    expected = 7
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve("10-input.txt")
    print(f"{result=}")
    assert result == 500, "Failed the large input"
    banner("end of part one (I)")

    banner("Started Part two (II)")
    result = solve("10-easy.txt")
    print(f"{result=}")
    assert result == 0, "Failed the easy input"

    result = solve("10-input.txt")
    print(f"{result=}")
    assert result == 0, "Failed the large input"

    print("All is good in da' hood.")
