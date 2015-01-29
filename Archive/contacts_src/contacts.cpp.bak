//g++ -Wall -o send send.cpp

#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <unistd.h>

#define GOOGLECSV "/home/josh/.mutt/google.csv"

using namespace std;

int main(int argc, char* argv[]) {

	string search;
	vector<string> nameArray;
	string line;
	unsigned int offset;
	bool first=true;

	ifstream google(GOOGLECSV);
	if (!google) {
		cout << "Cannot open input file" << endl;
		return 1;
	}

	do{
		if ((argc < 2) || (first == false)) {
			cout << "Search: ";
			cin >> search;
		}else{
			search = argv[1];
		}

		while(!google.eof() && (nameArray.size != 0)){
			getline(google,line);
			if ((offset = line.find(search, 0)) != string::npos) {
				string name;
				name = split(line, "<", 1);
				name = splitToNames(name);

				string email;
				email = split(line, "<", 2);
				email = email.substr(0, email.size()-1);

				nameArray.push_back(email);
			}
		}

		google.close();
