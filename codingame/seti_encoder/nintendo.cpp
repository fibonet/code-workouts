#include <array>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <span>
#include <string>
#include <vector>

using namespace std;

void hex_log(span<const uint32_t> arr, ostream& outs = cerr)
{
    for (const auto& value : arr)
    {
        outs << setfill('0') << setw(8) << hex << value << " ";
    }
    outs << endl;
}

inline bool are_equal(span<const uint32_t> a, span<const uint32_t> b)
{
    if (a.size() != b.size())
        return false;

    if (a.empty())
        return true;

    return memcmp(a.data(), b.data(), a.size() * sizeof(uint32_t)) == 0;
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

int main()
{
    array<uint32_t, MAX_SIZE> input;
    array<uint32_t, MAX_SIZE> force;

    size_t size;
    cin >> size;
    const size_t storeSize = size >> 4;

    for (size_t i = 0; i < size; i++)
    {
        cin >> hex >> input[i];
    }

    cerr << "Using " << size << " bits, stored as -> " << storeSize << " uints." << endl;
    cerr << "Read from stdin:" << endl;

    auto encoded_input = span<uint32_t>(span<uint32_t>(input.data(), storeSize));
    auto work = span<uint32_t>(span<uint32_t>(force.data(), storeSize));

    hex_log(encoded_input);

    for (uint32_t i = 0; i < 256; ++i)
    {
        for (uint32_t j = 0; j < 256; ++j)
        {
            force[0] = i;
            force[1] = j;
            auto result = encode(work, size);
            if (are_equal(encoded_input, result))
            {
                hex_log(work);
            }
        }
    }

    cout << "ANSWER" << endl;
}
