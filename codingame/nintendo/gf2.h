#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <ostream>
#include <span>
#include <string_view>
#include <tuple>

constexpr size_t MAX_WORDS = 16;

struct DivModResult
{
    size_t quot;
    size_t rem;
};

inline DivModResult divmod32(std::size_t x) noexcept { return { x >> 5, x & 31 }; }

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

    return {result.data(), coeff.size()};
}

std::span<uint32_t> gf2_fast_mul(const std::span<uint32_t> coeff)
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

    return {result.data(), coeff.size()};
}

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
