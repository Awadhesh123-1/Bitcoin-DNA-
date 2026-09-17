#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>

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
        ss << hex << setw(2) << setfill('0')
           << (int)hash[i];
    }

    return ss.str();
}

void show_help() {
    cout << "=== BTC-DNA BLOCKCHAIN ===" << endl;
    cout << endl;
    cout << "Usage:" << endl;
    cout << "  ./blockchain           Show blockchain data" << endl;
    cout << "  ./blockchain --help    Show this help" << endl;
    cout << endl;
    cout << "Features:" << endl;
    cout << "  SHA-256 hashing" << endl;
    cout << "  Bitcoin DNA / BTCDNA" << endl;
}

int main(int argc, char* argv[]) {

    if (argc > 1 && string(argv[1]) == "--help") {
        show_help();
        return 0;
    }

    string data = "Bitcoin DNA - BTCDNA";

    cout << "Data: " << data << endl;
    cout << "SHA-256: " << sha256(data) << endl;

    return 0;
}
