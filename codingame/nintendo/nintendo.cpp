#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <immintrin.h>
#include <iomanip>
#include <ios>
#include <iostream>
#include <span>
#include <string>
#include <vector>
#include <wmmintrin.h>

using namespace std;

struct u256
{
    __m128i lo;
    __m128i hi;
};

// Carry-less multiply two 128-bit values (a, b) over GF(2).
// Output is full 256-bit polynomial product.
static inline u256 gf2_clmul_128(const __m128i& a, const __m128i& b)
{
    // Low parts
    __m128i x0 = _mm_clmulepi64_si128(a, b, 0x00); // a_low  * b_low
    // Cross terms
    __m128i x1 = _mm_clmulepi64_si128(a, b, 0x01); // a_low  * b_high
    __m128i x2 = _mm_clmulepi64_si128(a, b, 0x10); // a_high * b_low
    // High parts
    __m128i x3 = _mm_clmulepi64_si128(a, b, 0x11); // a_high * b_high

    // Now combine the middle terms.
    __m128i mid = _mm_xor_si128(x1, x2);

    // Shift + combine to form full 256-bit result
    __m128i mid_lo = _mm_slli_si128(mid, 8); // shift left 64 bits
    __m128i mid_hi = _mm_srli_si128(mid, 8); // shift right 64 bits

    u256 r;
    r.lo = _mm_xor_si128(x0, mid_lo);
    r.hi = _mm_xor_si128(x3, mid_hi);

    return r;
}

static void print_u128(const __m128i& v)
{
    uint64_t hi = _mm_extract_epi64(v, 1);
    uint64_t lo = _mm_extract_epi64(v, 0);
    std::cout << std::hex << std::setfill('0') << std::setw(16) << hi << "_"
              << std::setw(16) << lo;
}

void hex_log(span<const uint32_t> arr, ostream& outs = cerr)
{
    for (const auto& value : arr)
    {
        outs << setfill('0') << setw(8) << hex << value << " ";
    }
    outs << endl;
}

const int MAX_SIZE = 32;
static std::array<uint32_t, MAX_SIZE> buffer;

span<uint32_t> encode(span<const uint32_t> data, size_t bits)
{
    uint32_t store_size = bits / 16;
    uint32_t words = bits / 32;

    buffer.fill(0);

    for (uint32_t i = 0; i < bits; ++i)
    {
        auto pi = div(i, 32);

        uint32_t bit_i = (data[pi.quot] >> pi.rem) & 1U;

        for (uint32_t j = 0; j < bits; ++j)
        {
            auto pj = div(j, 32);
            auto po = div(i + j, 32);
            uint32_t bit_j = (data[pj.quot + words] >> pj.rem) & 1U;

            buffer[po.quot] ^= (bit_i & bit_j) << po.rem;
        }
    }

    return span<uint32_t>(buffer.data(), store_size);
}

uint64_t gf2_reverse_poly_fast(uint64_t x)
{
    if (x == 0)
        return 0;

    // Full 64-bit bit-reversal
    uint64_t r = x;
    r = ((r & 0x5555555555555555ULL) << 1) | ((r >> 1) & 0x5555555555555555ULL);
    r = ((r & 0x3333333333333333ULL) << 2) | ((r >> 2) & 0x3333333333333333ULL);
    r = ((r & 0x0F0F0F0F0F0F0F0FULL) << 4) | ((r >> 4) & 0x0F0F0F0F0F0F0F0FULL);
    r = ((r & 0x00FF00FF00FF00FFULL) << 8) | ((r >> 8) & 0x00FF00FF00FF00FFULL);
    r = (r << 48) | ((r & 0xFFFF0000ULL) << 16) | ((r >> 16) & 0xFFFFULL) | (r >> 48);

    // remove leading zeros lost by reversal
    int deg = 63 - std::countl_zero(x);
    r >>= (64 - deg - 1);

    return r;
}

int main()
{
    // weird upfront size init
    size_t size;
    cin >> size;
    const size_t storeSize = size >> 4;
    cerr << "Working " << storeSize << " ints of " << size << " bits." << endl;

    array<uint32_t, MAX_SIZE> input;
    auto encoded_input = span<uint32_t>(span<uint32_t>(input.data(), storeSize));

    uint64_t aaa = 0U;
    for (size_t i = 0; i < storeSize; i++)
    {
        cin >> hex >> input[i];
        aaa |= input[i] << (size * i);
    }

    cerr << "Read from stdin:" << endl;
    hex_log(encoded_input);
    cerr << "one " << hex << setfill('0') << setw(16) << aaa << endl;

    // __m128i a = _mm_set_epi64x(0, 0xb0c152f9ULL);
    // __m128i b = _mm_set_epi64x(0, 0xebf2831fULL);
    //
    // std::cout << "high: ";
    // print_u128(a);
    // std::cout << "\n";
    // std::cout << "low : ";
    // print_u128(b);
    // std::cout << "\n";
    //
    // u256 r = gf2_clmul_128(a, b);
    //
    // std::cout << "a * b over GF(2):\n";
    // std::cout << "high: ";
    // print_u128(r.hi);
    // std::cout << "\n";
    // std::cout << "low : ";
    // print_u128(r.lo);
    // std::cout << "\n";

    uint64_t cc = 0x46508fb7;
    uint64_t bb = 0x6677e201;
    cout << hex << cc << " x " << bb << endl;
    uint64_t rr;

    uint64_t aa = gf2_reverse_poly_fast(cc);
    cout << hex << aa << endl;

    cout << "ANSWER" << endl;
}
