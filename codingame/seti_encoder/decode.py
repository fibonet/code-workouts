#!/usr/bin/env python3

from typing import Sequence


def log_array(values: Sequence, size: int, name="", prefix=""):
    if name:
        print(f"{name.title()}")

    for value in values[: size // 16]:
        print(f"{value:08x}x  {prefix}{value:032b}  // ({value.bit_length():2} bits)")


def expand(n: int) -> list[tuple]:
    result = list()
    for i in range(n + 1):
        result.append((i, n - i))
    return result


def encode(data: Sequence, size: int):
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

    return buffer[:store_size]


def mask(data: Sequence, size: int):
    store_size = size // 16
    buffer = [0] * store_size

    for i in range(size):
        for j in range(size):
            pos_i, shift_i = divmod(i, 32)
            pos_j, shift_j = divmod(j, 32)
            pos_out, shift_out = divmod(i + j, 32)

            bit = (data[pos_out] >> shift_out) & 1
            if bit:
                pass
                # buffer[pos_i] |= bit << shift_i
                # buffer[pos_j + size // 32] |= bit << shift_j
            else:
                buffer[pos_i] ^= (1 - bit) << shift_i
                buffer[pos_j + size // 32] ^= (1 - bit) << shift_j

    return buffer


def main(filename: str):
    print("--" * 20)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    size, encoded = content.split("\n")
    size = int(size)
    print("Working with", size, "bits")
    encoded = [int(val, 16) for val in encoded.split()]
    log_array(encoded, size, "read")

    # brutte force
    # for a in range(256):
    #     for b in range(256):
    #         data = (a, b)
    #         result = encode(data, size)
    #         if result == encoded:
    #             log_array(data, size, "found")

    data = (0x83, 0xe5)
    log_array(data, size, "sample")
    result = encode(data, size)
    log_array(result, size, "all ones")

    mm = mask(result, size)
    log_array(mm, size, "mask")


if __name__ == "__main__":
    main("input.txt")
