#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <ostream>
#include <span>
#include <string_view>
#include <tuple>
#include <type_traits>

constexpr size_t MAX_WORDS = 16;

struct DivModResult
{
    size_t quot;
    size_t rem;
};

inline DivModResult divmod32(std::size_t x) noexcept { return { x >> 5, x & 31 }; }

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

uint32_t shift_left(std::array<uint32_t, MAX_WORDS>& poly, size_t words)
{
    uint32_t carry { 0 };
    for (size_t i = 0; i < words; ++i)
    {
        carry = poly[i] >> 31;
        poly[i] <<= 1;
    }
    return carry;
}

void gf2_add(
    std::array<uint32_t, MAX_WORDS>& dest,
    size_t at_bit,
    std::span<uint32_t> source,
    size_t words
)
{
    uint32_t low;
    uint32_t high;
    for (size_t wi = 0; wi < words; ++wi)
    {
        low = source[wi] >> at_bit;
        high = source[wi + 1] & (~0u >> (32 - at_bit));

        std::cout << std::format("add {}..{} / {}b  {}B", wi, words, at_bit, 32-at_bit) << std::endl;
        std::cout << std::format("/{:32b} {:32b}/", high, low) << std::endl;

        dest[wi] ^= low;
    }
}

std::span<uint32_t> gf2_fast_mul(const std::span<uint32_t> coeff)
{
    const size_t mid { coeff.size() >> 1 };
    static std::array<uint32_t, MAX_WORDS> result;
    result.fill(0);
    for (size_t i = 0; i < mid; ++i)
    {
        const auto po = divmod32(i);
        const auto bit_left = (coeff[po.quot] >> po.rem) & 1;
        if (bit_left)
        {
            gf2_add(result, i, coeff.subspan(mid, mid), mid);
        }
    }

    std::cout << std::endl;
    return { result.data(), coeff.size() };
}

bool gf2_equal(const std::span<uint32_t>& left, const std::span<uint32_t>& right)
{
    if (left.size() != right.size())
        return false;
    return std::memcmp(left.data(), right.data(), left.size() * sizeof(uint32_t)) == 0;
}

/***
 * Performs Polynomial multiplication in GF2
 */
std::span<uint32_t> gf2_mul(const std::span<uint32_t> coeff)
{
    static std::array<uint32_t, MAX_WORDS> result;
    result.fill(0);

    const size_t bits = coeff.size() << 4;
    const size_t midp = coeff.size() >> 1;

    for (size_t i = 0; i < bits; ++i)
    {
        auto pi = divmod32(i);
        if ((coeff[pi.quot] >> pi.rem) & 1)
        {
            for (size_t j = 0; j < bits; ++j)
            {
                auto pj = divmod32(j);
                auto right_bit = (coeff[pj.quot + midp] >> pj.rem) & 1;
                auto po = divmod32(i + j);
                result[po.quot] ^= right_bit << po.rem;
            }
        }
    }

    return { result.data(), coeff.size() };
}
