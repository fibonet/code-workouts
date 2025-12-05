#!/usr/bin/env python3


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    lines = iter(content.split("\n"))

    fresh_ranges = list()
    while line := next(lines):
        start, stop = map(int, line.split("-"))
        fresh_ranges.append((start, stop))

    fresh_ranges.sort()
    print(f"{fresh_ranges=}")

    fresh_count = 0
    for line in lines:
        iid = int(line)
        for start, stop in fresh_ranges:
            if start <= iid <= stop:
                fresh_count += 1
                break

    print(f"Found {fresh_count} ingredients.")

    checklist = list()
    fresh_size = 0

    for start, stop in fresh_ranges:
        for prev_start, prev_stop in checklist:
            if prev_start <= start <= prev_stop:
                print((start, stop), "overlaps", (prev_start, prev_stop))

                if stop > prev_stop:
                    start = prev_stop + 1
                else:
                    print("completely subincluded")
                    break

        else:
            checklist.append((start, stop))
            fresh_size += stop - start + 1

    print(len(checklist), "vs", len(fresh_ranges))
    print("Total fresh ids:", fresh_size)


if __name__ == "__main__":
    main("05-input.txt")
