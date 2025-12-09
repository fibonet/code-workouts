#include "gf2.h"

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <span>

void manual_testing()
{
    std::array<uint32_t, 2> ab1 { 0xffffffff, 0x5555aaaa };
    pretty_hexbin(std::span { ab1.data(), ab1.size() }, "AB1");

    auto r1 = gf2_mul(std::span { ab1.data(), ab1.size() });
    pretty_hexbin(std::span { r1.data(), ab1.size() }, "Q");

    std::array<uint32_t, 2> ab2 { 0xe5, 0x83 };
    pretty_hexbin(std::span { ab2.data(), ab2.size() }, "AB2");
    auto r2 = gf2_mul(std::span { ab2.data(), ab2.size() });
    pretty_hexbin(std::span { r2.data(), ab1.size() }, "R");
}

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

    pretty_hexbin(std::span { input.data(), store_size }, "in");

    auto res = gf2_mul(std::span { input.data(), store_size });
    pretty_hexbin(std::span { res.data(), store_size }, "mul");

    manual_testing();

    return 0;
}
