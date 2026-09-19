#include <bits/stdc++.h>
using namespace std;

string xor_op(const string &a, const string &b) {
    string res;
    for (int i = 0; i < a.length(); i++)
        res += (a[i] == b[i]) ? '0' : '1';
    return res;
}

string compute_crc(string data, string generator) {
    int g = generator.length();
    int r = g - 1;

    string padded = data + string(r, '0');
    string temp = padded.substr(0, g);
    int idx = g;

    while (idx <= padded.length()) {
        if (temp[0] == '1')
            temp = xor_op(temp, generator);
        else
            temp = xor_op(temp, string(g, '0'));

        if (idx < padded.length())
            temp = temp.substr(1) + padded[idx];
        idx++;
    }

    return temp.substr(temp.length() - r);
}

int main() {

    string data = "1010101010";
    string generator = "110101";
    int r = generator.length() - 1;

    cout << "Original Data: " << data << endl;
    cout << "Generator Polynomial: " << generator << endl;

    string crc = compute_crc(data, generator);
    string transmitted = data + crc;

    cout << "CRC: " << crc << endl;
    cout << "Transmitted Frame: " << transmitted << endl;

    string received = transmitted;
    srand(time(0));
    int pos = rand() % received.length();
    received[pos] = (received[pos] == '0') ? '1' : '0';

    cout << "Received Frame (error at position " << pos << "): "
         << received << endl;

    string remainder = compute_crc(received, generator);

    bool error = false;
    for (char c : remainder)
        if (c == '1') error = true;

    if (error)
        cout << "Frame Discarded (Error Detected)" << endl;
    else
        cout << "Frame Accepted (No Error Detected)" << endl;

    return 0;
}

