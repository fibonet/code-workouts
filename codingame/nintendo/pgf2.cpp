#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string_view>

constexpr size_t N = 32;
constexpr size_t N2 = N / 2;
constexpr unsigned long long LOWQ = ((1ULL << N2) - 1);

template <int SIZE>
void print(const std::bitset<SIZE>& value, std::string_view name, size_t group = SIZE / 2)
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
    std::cout << " 0x" << std::hex << std::setfill('0') << std::setw(N / 4) << numeric;

    std::cout << std::endl;
}

std::bitset<2 * N> pgf2_mul(const std::bitset<N>& a, const std::bitset<N>& b)
{
    uint64_t A = a.to_ullong();
    uint64_t B = b.to_ullong();
    uint64_t C { 0ULL };

    while (B)
    {
        if (B & 1)
        {
            C ^= A;
        }
        B >>= 1;
        A <<= 1;
    }

    return std::bitset<2 * N> { C };
}

void test_01()
{
    std::bitset<N> a { 0xebf2831f };
    std::bitset<N> b { 0xb0c152f9 };
    std::bitset<2 * N> a_encoded { 0x0000000073af };

    print<N>(a, "A");
    print<N>(b, "B");

    auto r2 = pgf2_mul(a, b);
    print<2 * N>(r2, "C");
}

int main() { test_01(); }
