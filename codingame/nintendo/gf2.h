#pragma once

#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <ostream>
#include <string_view>

/***
 * Pretty prints as grouped binary and hex format
 */
template <size_t SIZE>
void pretty_hexbin(
    const std::bitset<SIZE>& value,
    std::string_view name,
    std::ostream& output = std::cerr,
    size_t group = SIZE / 2
)
{
    std::cout << name << ": ";
    for (size_t i = SIZE; i > 0; --i)
    {
        std::cout << value[i - 1];
        if ((i - 1) % group == 0)
        {
            std::cout << " ";
        }
    }
    auto numeric = value.to_ullong();
    output << " 0x" << std::hex << std::setfill('0') << std::setw(SIZE / 4) << numeric;
    output << std::endl;
}

/***
 * Performs Polynomial multiplication in GF2
 */
template <size_t SIZE>
std::bitset<SIZE> pgf2_mul(std::bitset<SIZE>& A, std::bitset<SIZE>& B)
{
    std::bitset<SIZE> C;
    while (B.any())
    {
        if (B.test(0))
        {
            C ^= A;
        }
        B >>= 1;
        A <<= 1;
    }

    return C;
}
