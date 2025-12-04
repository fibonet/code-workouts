#!/usr/bin/env python3
from itertools import combinations


def find_max_joltage(banks: list[str]) -> int:
    total = 0

    for bank in banks:
        pairs = set()
        for pair in combinations(bank, 2):
            pairs.add(int("".join(pair)))
        total += max(pairs)

    return total


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    banks = content.split("\n")
    joltage = find_max_joltage(banks)
    print(f"The {len(banks)} banks can produce a maximum of {joltage} jolts.")


if __name__ == "__main__":
    main("03-input.txt")
