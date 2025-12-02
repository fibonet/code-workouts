#include <algorithm>
#include <iomanip>
#include <iostream>
#include <span>
#include <string>
#include <vector>

using namespace std;

void log(span<const unsigned int> arr, ) {
    for (const auto &value : arr) {
        cerr << setfill('0') << setw(8) << hex << value << " ";
    }
    cerr << endl;
}

vector<unsigned int> encode(span<const unsigned int> data, size_t size) {
    vector<unsigned int> encoded(data.size(), 0);

    for (size_t i = 0; i < size; i++) {
        for (size_t j = 0; j < size; j++) {
            encoded[(i + j) / 32] ^=
                ((data[i / 32] >> (i % 32)) &
                 (data[j / 32 + size / 32] >> (j % 32)) & 1)
                << ((i + j) % 32);
        }
    }

    return encoded;
}

vector<unsigned int> decode(span<const unsigned int> encoded, size_t size) {
    vector<unsigned int> decoded(encoded.size(), 0);

    // For each bit position in encoded
    for (size_t i = 0; i < size; i++) {
        for (size_t j = 0; j < size; j++) {
            cerr << dec << i << "," << j << " : " << i + j << " ~ "
                 << (i + j) / 32 << endl;

            decoded[(i + j) / 32] ^=
                ((encoded[i / 32] >> (i % 32)) &
                 (encoded[j / 32 + size / 32] >> (j % 32)) & 1)
                << ((i + j) % 32);
        }
    }

    return decoded;
}

int main() {
    size_t size;
    cin >> size;
    const size_t storeSize = size >> 4;

    vector<unsigned int> input(storeSize);
    for (size_t i = 0; i < size; i++) {
        cin >> hex >> input[i];
    }

    cerr << "Using " << size << " bits, stored as -> " << storeSize << " uints."
         << endl;
    cerr << "Read from stdin:" << endl;
    log(input);

    vector<unsigned int> play = decode(input, size);

    cerr << "new shit decoder:" << endl;
    log(play);

    cout << "ANSWER" << endl;
}
