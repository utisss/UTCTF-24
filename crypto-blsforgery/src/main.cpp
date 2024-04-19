#include <bls12-381/bls12-381.hpp>
#include <iostream>
#include <random>
#include <fstream>
#include <charconv>

using namespace std;
using namespace bls12_381;

std::array<uint8_t, 32> getRandomSeed() {
    std::array<uint64_t, 4> buf;
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<uint64_t> dis;
    buf[0] = dis(gen);
    buf[1] = dis(gen);
    buf[2] = dis(gen);
    buf[3] = dis(gen);
    std::array<uint8_t, 32> res;
    memcpy(res.data(), buf.data(), sizeof(res));
    return res;
}

int main() {
    string agreement = "Bob and I signed the deal.";
    vector<uint8_t> ag_vec(agreement.begin(), agreement.end());
    
    array<uint64_t, 4> bob_sk = secret_key(getRandomSeed());
    g1 bob_pk = public_key(bob_sk);
    for (uint8_t b : bob_pk.toAffineBytesLE()) {
        printf("%02x", b);
    }
    printf("\n");
    fflush(stdout);

    array<uint8_t, 96> data = {0};
    string input;
    getline(cin, input);
    if (input.length() != 192) return 0;
    for (size_t i = 0; i < input.length() / 2; ++i) {
        auto start = input.data() + i * 2;
        auto end = start + 2;
        unsigned int byte = 0;
        auto [ptr, ec] = from_chars(start, end, byte, 16);
        if (ec == errc::invalid_argument || ec == errc::result_out_of_range) return 0;
        data[i] = static_cast<uint8_t>(byte);
    }
    g1 adv_pk = g1::fromAffineBytesLE(data, true).value();

    array<uint8_t, 192> sigdata = {0};
    getline(cin, input);
    if (input.length() != 384) return 0;
    for (size_t i = 0; i < input.length() / 2; ++i) {
        auto start = input.data() + i * 2;
        auto end = start + 2;
        unsigned int byte = 0;
        auto [ptr, ec] = from_chars(start, end, byte, 16);
        if (ec == errc::invalid_argument || ec == errc::result_out_of_range) return 0;
        sigdata[i] = static_cast<uint8_t>(byte);
    }
    g2 adv_sig = g2::fromAffineBytesLE(sigdata, true).value();

    if (aggregate_verify(array{bob_pk, adv_pk}, array{ag_vec, ag_vec}, adv_sig)) {
        printf(":)\n");
        ifstream file("flag.txt");
        if (!file.is_open()) return -1;

        string line;
        getline(file, line);
        printf("%s\n", line.c_str());
        fflush(stdout);
        file.close();
    } else {
        printf(":(\n");
        fflush(stdout);
    }
}