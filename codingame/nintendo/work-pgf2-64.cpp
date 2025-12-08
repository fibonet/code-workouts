#include "gf2.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <span>

int main(void)
{
    std::array<uint32_t, MAX_WORDS> input {};
    size_t word_size;
    std::cin >> word_size;
    const size_t store_size = word_size >> 4;
    std::cerr << "Working with " << word_size << " bits, " << store_size << " words."
              << std::endl;

    for (size_t i = 0; i < store_size; i++)
    {
        std::cin >> std::hex >> input[i];
    }

    pretty_hexbin(std::span<uint32_t>(input.data(), store_size), "in");

    auto res = gf2_mul(
        std::span<uint32_t>(input.data(), store_size / 2),
        std::span<uint32_t>(input.data() + store_size / 2, store_size / 2)
    );
    pretty_hexbin(std::span<uint32_t>(res.data(), store_size), "mul");

    return 0;
}
