#!/usr/bin/env python3


def sum_invalid_ranges(ranges: list):
    count, total = 0, 0
    for range_spec in ranges:
        first, last = map(int, range_spec.split("-"))

        for value in range(first, last + 1):
            text = str(value)
            mid, r = divmod(len(text), 2)
            if r == 0 and text[:mid] == text[mid:]:
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
