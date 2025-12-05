#!/usr/bin/env python3
from collections import deque
from operator import itemgetter


def find_max_joltage(banks: list[str], size: int) -> int:
    total = 0

    for bank in banks:
        selected = deque()
        n = len(bank)
        first, last = 0, n - size + 1

        for i in range(size):
            last = n - (size - i) + 1
            available = bank[first:last]
            index, value = max(enumerate(available), key=itemgetter(1))

            selected.append(value)
            print(
                f"{i} [{first}:{last}] {available}, picking {value} => {''.join(selected)}"
            )
            first += index + 1

        print(bank, "=>", "".join(selected))
        total += int("".join(selected))

    return total


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    banks = content.split("\n")
    joltage = find_max_joltage(banks, 12)
    print(f"The {len(banks)} banks can produce a maximum of {joltage} jolts.")


if __name__ == "__main__":
    main("03-input.txt")
