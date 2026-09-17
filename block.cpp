#include <iostream>
#include <string>
#include <openssl/sha.h>
#include <sstream>
#include <iomanip>

using namespace std;

string sha256(const string& input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];

    SHA256(
        reinterpret_cast<const unsigned char*>(input.c_str()),
        input.size(),
        hash
    );

    stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << hex << setw(2) << setfill('0') << (int)hash[i];
    }

    return ss.str();
}

struct Block {
    int index;
    string previousHash;
    string data;
    string hash;
};

int main() {

    // ===== GENESIS BLOCK =====
    Block genesis;

    genesis.index = 0;
    genesis.previousHash = "0";
    genesis.data = "Genesis Block - BTCDNA";

    string genesisData =
        to_string(genesis.index) +
        genesis.previousHash +
        genesis.data;

    genesis.hash = sha256(genesisData);


    // ===== BLOCK #1 =====
    Block block1;

    block1.index = 1;
    block1.previousHash = genesis.hash;
    block1.data = "Block #1 - BTCDNA";

    string block1Data =
        to_string(block1.index) +
        block1.previousHash +
        block1.data;

    block1.hash = sha256(block1Data);


    // ===== DISPLAY =====
    cout << "=== BITCOIN DNA BLOCKCHAIN ===" << endl;

    cout << "\n--- GENESIS BLOCK ---" << endl;
    cout << "Index: " << genesis.index << endl;
    cout << "Previous Hash: " << genesis.previousHash << endl;
    cout << "Data: " << genesis.data << endl;
    cout << "Hash: " << genesis.hash << endl;

    cout << "\n--- BLOCK #1 ---" << endl;
    cout << "Index: " << block1.index << endl;
    cout << "Previous Hash: " << block1.previousHash << endl;
    cout << "Data: " << block1.data << endl;
    cout << "Hash: " << block1.hash << endl;

    return 0;
}
