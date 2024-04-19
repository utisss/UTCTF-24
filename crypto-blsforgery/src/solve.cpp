/*
from blspy import (AugSchemeMPL, Util, G1Element, G2Element)
from secrets import token_bytes
bob_pk = G1Element.from_bytes(bytes.fromhex(input("Bob's pk: ")))
inverse_bob_pk = bob_pk.negate()
adv_sk = AugSchemeMPL.key_gen(token_bytes(32))
forge_pk = adv_sk.get_g1() + inverse_bob_pk
print("Forged pk:", forge_pk)
print(AugSchemeMPL.sign(adv_sk, bytes.fromhex(input("Message: "))))
*/

#include <bls12-381/bls12-381.hpp>
#include <iostream>
#include <random>
#include <fstream>
#include <charconv>
#include <optional>

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
    g1 inverse_bob_pk = g1::fromAffineBytesLE(data, true).value().negate();

    array<uint64_t, 4> adv_sk = secret_key(getRandomSeed());
    g1 adv_pk = public_key(adv_sk);
    g1 forged_pk = adv_pk.add(inverse_bob_pk);
    for (uint8_t b : forged_pk.toAffineBytesLE()) {
        printf("%02x", b);
    }
    printf("\n");

    g2 forgery = sign(adv_sk, ag_vec);
    for (uint8_t b : forgery.toAffineBytesLE()) {
        printf("%02x", b);
    }
    printf("\n");
}