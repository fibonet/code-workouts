#include "gf2.h"

constexpr size_t BITS = 64;

void test_01()
{
    std::bitset<BITS> a { 0xebf2831f };
    std::bitset<BITS> b { 0xb0c152f9 };
    std::bitset<BITS> a_encoded { 0x0000000073af };

    pretty_hexbin<BITS>(a, "A");
    pretty_hexbin<BITS>(b, "B");

    auto res = pgf2_mul<BITS>(a, b);
    pretty_hexbin<BITS>(res, "C");
}

int main() { test_01(); }
