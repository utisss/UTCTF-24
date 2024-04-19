#include <thread>
#include <vector>
#include <cstdint>
#include <string>
#include <iostream>
#include <barrier>
#include <iomanip>

using namespace std;

const uint8_t SBOX[16][8] = {
    {2, 8, 6, 1, 3, 5, 4, 7},
    {6, 1, 4, 8, 5, 2, 3, 7},
    {7, 8, 3, 5, 1, 2, 4, 6},
    {4, 1, 3, 6, 2, 8, 5, 7},
    {7, 5, 8, 6, 1, 4, 3, 2},
    {7, 4, 8, 5, 6, 2, 3, 1},
    {7, 6, 4, 8, 1, 3, 2, 5},
    {3, 1, 8, 4, 7, 2, 6, 5},
    {3, 4, 8, 6, 2, 5, 1, 7},
    {8, 1, 6, 2, 7, 5, 4, 3},
    {2, 7, 5, 8, 1, 4, 3, 6},
    {3, 4, 2, 6, 5, 8, 7, 1},
    {1, 4, 3, 5, 7, 6, 2, 8},
    {4, 7, 3, 6, 5, 1, 8, 2},
    {6, 7, 4, 1, 5, 3, 2, 8},
    {3, 8, 4, 6, 7, 2, 5, 1},
};

uint8_t permute(uint8_t input, uint8_t threadidx) {
    uint8_t result = 0;
    for (uint8_t i = 0; i < 8; i++) {
        if (input & (1 << i)) result |= (1 << (SBOX[threadidx - 1][i] - 1));
    }
    return result;
}

vector<uint8_t> HexToBytes(const string& hex) {
    vector<uint8_t> bytes;

    for (unsigned int i = 0; i < hex.length(); i += 2) {
        string byteString = hex.substr(i, 2);
        uint8_t byte = (uint8_t) strtoul(byteString.c_str(), NULL, 16);
        bytes.push_back(byte);
    }

    return bytes;
}

void hasher(barrier<>& bar, vector<uint8_t>& workspace, uint8_t threadidx) {
    for (int block = 0; block < workspace.size(); block += 16) {
        for (int intidx = threadidx, cnt = 0; cnt < 16; cnt++, intidx = (intidx * 7) % 17) {
            int loc = block + intidx;
            workspace[loc] = permute(workspace[loc], threadidx);
            bar.arrive_and_wait();
        }
    }
}

int main() {
    string input;
    getline(cin, input);
    vector<uint8_t> input_arr = HexToBytes(input);
    vector<uint8_t> padding(16 - (input_arr.size() % 16), 0);
    input_arr.insert(input_arr.end(), padding.begin(), padding.end());

    thread workers[16];
    barrier blocker(16);
    for (uint8_t t = 1; t <= 16; t++) {
        workers[t - 1] = thread(hasher, ref(blocker), ref(input_arr), t);
    }
    
    for (int i = 0; i < 16; i++) workers[i].join();

    printf("%ld\n\n", input_arr.size());
    for (int i = 0; i < input_arr.size() - padding.size(); i++) cout << hex << setfill('0') << setw(2) << static_cast<int>(input_arr[i]);
}