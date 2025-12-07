#!/usr/bin/env python3
from collections import defaultdict
from functools import lru_cache
from typing import Sequence


def log_array(values: Sequence, size: int, name="", prefix=""):
    if name:
        print(f"{name.title()}")

    for value in values[: size // 16]:
        print(f"{value:08x}x  {prefix}{value:032b}  // ({value.bit_length():2} bits)")


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


def alt_encode(pair: tuple[int]):
    a, b = pair
    res = 0
    count = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        b >>= 1
        count += 1
    return res


def prime_factorisation(number: int) -> list[int]:
    if number < 2:
        return []

    factors = list()
    n = number
    while (qr := divmod(n, 2))[1] == 0:
        factors.append(2)
        n = qr[0]

    p = 3
    while p * p <= n:
        while (qr := divmod(n, p))[1] == 0:
            factors.append(p)
            n = qr[0]
        p += 2

    if n > 1:
        factors.append(n)

    return factors


def factor_pairs(n: int, size: int) -> list[tuple[int, int]]:
    if n == 0:
        return []

    factors = list()
    for i in range(1, size):
        for j in range(1, size):
            prod, rem = divmod(i * j, size)
            if rem == 0:
                factors.append((i, j))

    return factors


def main(filename: str):
    print("--" * 20)
    with open(filename, "rt") as file:
        content = file.read().strip()
        print("read", len(content), "bytes from", filename)

    word_size, words = content.split("\n")
    word_size = int(word_size)
    print("Working with", word_size, "bit words")

    encoded = [int(word, 16) for word in words.split()]
    log_array(encoded, word_size, "read:")

    map = defaultdict(list)
    N = 256
    for a in range(N):
        for b in range(N):
            data = (a, b)
            enc = alt_encode(data)
            map[enc].append(data)

    for value in sorted(map.keys()):
        print(f"{value:08b} {value}", "->", sorted(map[value]))
        # print("\t\t", end="")
        # for pair in sorted(map[value]):
        #     print(f"({pair[0]:06b} {pair[1]:06b})", end=" ")
        # print()


if __name__ == "__main__":
    main("input.txt")
