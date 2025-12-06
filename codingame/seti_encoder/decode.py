#!/usr/bin/env python3


def log_bin(values: list, size: int, name="", prefix=""):
    if name:
        print(f"{name.title()}")

    for value in values:
        print(f"{prefix}{value:032b} ({value:08x}) // {value}")


def bin_to_grey(val: int):
    return val ^ (val >> 1)


def encode(data: list, size: int):
    store_size = size // 16
    encoded = [0] * store_size

    for i in range(size):
        for j in range(size):
            pos_i, shift_i = divmod(i, 32)
            pos_j, shift_j = divmod(j, 32)
            pos_out, shift_out = divmod(i + j, 32)

            bit_i = (data[pos_i] >> shift_i) & 1
            bit_j = (data[pos_j + size // 32] >> shift_j) & 1
            encoded[pos_out] ^= (bit_i & bit_j) << shift_out

    return encoded


def main(filename: str):
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    size, encoded = content.split("\n")
    size = int(size)
    print(f"{size} bits")

    encoded = [int(val, 16) for val in encoded.split()]
    decoded = encoded.copy()

    mmm = 0

    for b1 in range(9):
        for b2 in range(64):
            encoded = [b1, b2]
            decoded = encode(encoded, size)
            log_bin(encoded, size, "encoded input")
            log_bin(decoded, size, prefix=" => ")

    print(mmm)


if __name__ == "__main__":
    main("ff-input.txt")
