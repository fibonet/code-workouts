#include <iomanip>
#include <iostream>

using namespace std;

void print(unsigned int arr[], int size) {
    for (int i = 0; i < size; i++) {
        if (i > 0) {
            cerr << ' ';
        }
        cerr << setfill('0') << setw(8) << hex << arr[i];
    }
    cerr << endl;
}

int main() {
    int ss;
    cin >> ss;
    const int size = ss >> 4;
    unsigned int a[size];
    unsigned int b[size];
    unsigned int input[size];

    for (int i = 0; i < size; i++) {
        cin >> hex >> input[i];
    }

    unsigned int bb = 3;
    for (int ai = 0; ai < 16; ai++) {
        std::fill(b, b + size, 0);
        std::fill(a, a + size, 0);

        a[0] = bb;
        a[1] = bb;
        bb <<= 1;

        for (int i = 0; i < size; i++) {
            const int ih = i >> 5;
            const int il = i & 31;

            for (int j = 0; j < size; j++) {
                const int jh = j >> 5;
                const int jl = j & 31;

                cerr << i << "," << j << ":" << (i + j) / 32 << endl;
                b[(i + j) / 32] ^= ((a[i / 32] >> (i % 32)) &
                                    (a[j / 32 + size / 32] >> (j % 32)) & 1)
                                   << ((i + j) % 32);
            }
        }

        cerr << "--- " << ai << " ---" << endl;
        print(a, size);
        print(b, size);
    }

    return 0;
}
