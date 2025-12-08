#pragma once

#include <array>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <ostream>
#include <span>
#include <string_view>
#include <tuple>

constexpr size_t MAX_WORDS = 16;

/***
 * Pretty prints as grouped binary and hex format
 */
void pretty_hexbin(
    const std::span<uint32_t> values,
    std::string_view name,
    std::ostream& print = std::cerr
)
{
    print << name << ":" << std::endl;
    for (size_t i = values.size(); i > 0; --i)
    {
        const auto value = values[i - 1];
        print << std::format("[{:2}] ", i - 1) << std::format(" x{:08x} ", value)
              << std::format(" b{:032b}", value) << std::endl;
    }
}

/***
 * Performs Polynomial multiplication in GF2
 */
std::array<uint32_t, MAX_WORDS>
gf2_mul(const std::span<uint32_t> left, const std::span<uint32_t> right)
{
    std::array<uint32_t, MAX_WORDS> result {};

    for (size_t i = 0; i < (left.size() << 5); ++i)
    {
        auto pi = std::div(i, 32);
        auto left_bit = (left[pi.quot] >> pi.rem) & 1;
        for (size_t j = 0; j < (right.size() << 5); ++j)
        {
            auto pj = std::div(j, 32);
            auto right_bit = (right[pj.quot] >> pj.rem) & 1;
            auto po = div(i + j, 32);
            result[po.quot] ^= (left_bit & right_bit) << po.rem;
        }
    }

    return result;
}
