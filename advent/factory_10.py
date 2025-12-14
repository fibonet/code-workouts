#!/usr/bin/env python3
from collections import deque
from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Tuple

from pulp import PULP_CBC_CMD, LpInteger, LpMinimize, LpProblem, LpVariable, lpSum


def banner(name: str):
    size = 4 + len(name)
    print("*" * size)
    print(f"* {name.title()} *")
    print("*" * size)


@dataclass
class Machine:
    required_lights: int = 0
    size: int = 0
    specs: str = ""
    buttons: List = field(default_factory=list)
    button_masks: List = field(default_factory=list)
    button_increments: List = field(default_factory=list)
    required_jolts: Tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for token in self.specs.split():
            if token.startswith("["):
                values = token.strip("[]")[::-1]
                self.required_lights = int(
                    values.replace("#", "1").replace(".", "0"), 2
                )
                self.size = len(values)
            elif token.startswith("("):
                values = list(map(int, token.strip("()").split(",")))
                self.buttons.append(values)
                print(">>", self.buttons)
                # create bitmask
                self.button_masks.append(sum(1 << i for i in values))
                # create increment vector
                inc = [int(i in values) for i in range(self.size)]
                self.button_increments.append(inc)
            elif token.startswith("{"):
                self.required_jolts = tuple(map(int, token.strip("{}").split(",")))

    def __str__(self) -> str:
        lights = f"{self.required_lights:0{self.size}b}"
        joltage = ", ".join(map(str, self.required_jolts))
        buttons = ", ".join(map(lambda tu: format(tu, "b"), self.button_masks))
        increments = ", ".join(str(bi) for bi in self.button_increments)
        butts = ", ".join(map(str, self.buttons))
        return "\n".join(
            (
                "raw",
                self.specs,
                "machina goals",
                lights,
                joltage,
                "machina wirings",
                buttons,
                increments,
                butts,
            )
        )

    def solve_lights(self):
        trail = {0: (None, None)}
        queue = deque()
        state = 0
        while state != self.required_lights:
            for bi in self.button_masks:
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
        size_buttons = len(self.buttons)
        size_counter = self.size

        problem = LpProblem("MinButtonPresses", LpMinimize)
        X = [
            LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(size_buttons)
        ]
        problem += lpSum(X)

        for c in range(size_counter):
            problem += (
                lpSum(
                    X[bi] if c in self.buttons[bi] else 0 for bi in range(size_buttons)
                )
                == self.required_jolts[c]
            )
        problem.solve(PULP_CBC_CMD(msg=False))

        total = int(sum(xi.varValue or 0 for xi in X))
        solution = [int(xi.varValue or 0) for xi in X]
        return total, solution


def solve_for_lights(filename: str):
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


def solve_for_jolts(filename: str):
    banner(f"Solving {filename}")
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    machines = [Machine(specs=line) for line in content.split("\n")]

    count = 0
    for machine in machines:
        print(machine)
        total, push_log = machine.solve_joltage()
        pretty_log = " > ".join(format(i) for i in push_log)
        print(total, "push_log", pretty_log)
        count += total

    return count


if __name__ == "__main__":
    banner("Started Part one (I)")
    result = solve_for_lights("10-easy.txt")
    print(f"{result=}")
    expected = 7
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve_for_lights("10-input.txt")
    print(f"{result=}")
    assert result == 500, "Failed the large input"
    banner("end of part one (I)")

    banner("Started Part two (II)")
    result = solve_for_jolts("10-easy.txt")
    print(f"{result=}")
    expected = 33
    assert result == expected, f"Computed {result} was expected to be {expected}."

    result = solve_for_jolts("10-input.txt")
    print(f"{result=}")
    assert result == 19763, "Failed the large input"

    print("All is good in da' hood.")
