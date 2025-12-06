#!/usr/bin/env python3


def log_bin(values: list, size: int, name="", prefix=""):
    if name:
        print(f"{name.title()}")

    for value in values[: size // 16]:
        print(f"{prefix}{value:032b} {value:08x}x // {value} ({value.bit_length()})")


def bin_to_grey(val: int):
    return val ^ (val >> 1)


def expand(n: int) -> list[tuple]:
    result = list()
    for i in range(n + 1):
        result.append((i, n - i))
    return result




def encode(data: list, size: int):
    store_size = size // 16
    buffer = [0] * store_size

    for i in range(size):
        for j in range(size):
            pos_i, shift_i = divmod(i, 32)
            pos_j, shift_j = divmod(j, 32)
            pos_out, shift_out = divmod(i + j, 32)

            bit_i = (data[pos_i] >> shift_i) & 1
            bit_j = (data[pos_j + size // 32] >> shift_j) & 1
            buffer[pos_out] ^= (bit_i & bit_j) << shift_out

    return buffer


def mask(data: list, size: int):
    store_size = size // 16
    buffer = [0] * store_size

    count = [0] * (size * 2)
    for i in range(size):
        for j in range(size):
            pos_i, shift_i = divmod(i, 32)
            pos_j, shift_j = divmod(j, 32)
            pos_out, shift_out = divmod(i + j, 32)

            count[i + j] += 1

    print(count)
    return buffer


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    size, encoded = content.split("\n")
    size = int(size)
    print(size, "bits")
    encoded = [int(val, 16) for val in encoded.split()]

    log_bin(encoded, size, "looking around")
    mm = mask(encoded, size)

    log_bin(mm, size, "masked")


if __name__ == "__main__":
    main("input.txt")
