#include "gf2.h"

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <span>

struct MultiplyFixture
{
    size_t word_size;
    std::string words;
    std::string expected;
};

void nintendo_test_cases()
{
    const MultiplyFixture DATA[] {
        // DO nOt MoVe this shit *** exepected is in big endian order... why
        { 32, "00000001 000073af", "000073af 00000000" },
        { 32, "00000083 000000e5", "000073af 00000000" },
        { 32, "000000e5 00000083", "000073af 00000000" },
        { 32, "000073af 00000001", "000073af 00000000" },
        { 32, "00000001 738377c1", "738377c1 00000000" },
        { 32, "0000b0c5 0000cd55", "738377c1 00000000" },
        { 32, "0000cd55 0000b0c5", "738377c1 00000000" },
        { 32, "738377c1 00000001", "738377c1 00000000" },
        { 32, "b0c152f9 ebf2831f", "46508fb7 6677e201" },
        { 32, "ebf2831f b0c152f9", "46508fb7 6677e201" },
        { 64, "0cf5c2bf 9aba68ef c18fb79b de70eef7",
          "f3268b49 661859eb 0b324559 65ee6bda" },
        { 64, "c18fb79b de70eef7 0cf5c2bf 9aba68ef",
          "f3268b49 661859eb 0b324559 65ee6bda" },
        { 128, "a30d28bd bda19675 3f95d074 b6f69434 c58f4047 d73fe36a 24be2846 e2ebe432",
          "a91db473 fcea8db4 f3bb434a 8dba2f16 51abc87e 92c44759 5c1a16d3 6111c6f4" },
        { 128, "c58f4047 d73fe36a 24be2846 e2ebe432 a30d28bd bda19675 3f95d074 b6f69434",
          "a91db473 fcea8db4 f3bb434a 8dba2f16 51abc87e 92c44759 5c1a16d3 6111c6f4" },
        { 256,
          "320a18d5 b61b13f6 1aaaa61c 0afe2a41 1a4ff107 84cc2efc 956ff31d fa595299 "
          "33749a7f 6cc9659d dc503569 ef4d0ef5 73b746c5 b8fb36d3 7616e9d6 b21251c4",
          "4af6fc33 39029380 465c5267 c72f6a8b 0906e6d0 ca60550f 14a5e47c 42ad10fb "
          "4a3bb446 bb74360a 5ea02b9c 23c68553 3fade253 e270ba24 39e141ad 6c38c43d" },
        { 256,
          "33749a7f 6cc9659d dc503569 ef4d0ef5 73b746c5 b8fb36d3 7616e9d6 b21251c4 "
          "320a18d5 b61b13f6 1aaaa61c 0afe2a41 1a4ff107 84cc2efc 956ff31d fa595299",
          "4af6fc33 39029380 465c5267 c72f6a8b 0906e6d0 ca60550f 14a5e47c 42ad10fb "
          "4a3bb446 bb74360a 5ea02b9c 23c68553 3fade253 e270ba24 39e141ad 6c38c43d" }
    };

    for (const MultiplyFixture& it : DATA)
    {
        std::cout << std::format("[ {:3}b ]  ", it.word_size) << it.words << std::endl;
    }
}

int main(void)
{
    nintendo_test_cases();

    return 0;
}
