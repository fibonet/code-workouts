#!/usr/bin/env python3
import re


def sum_invalid_ranges(ranges: list):
    count, total = 0, 0
    has_repeated_sequence = re.compile(r"^(\d+)\1+$")
    for range_spec in ranges:
        first, last = map(int, range_spec.split("-"))
        for value in range(first, last + 1):
            text = str(value)
            if has_repeated_sequence.match(text):
                count += 1
                total += value

    return count, total


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    ranges = content.split(",")
    count, sum = sum_invalid_ranges(ranges)

    print(f"found {count} invalid ranges that add up to {sum}.")


if __name__ == "__main__":
    main("02-input.txt")
