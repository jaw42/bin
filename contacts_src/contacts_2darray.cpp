//g++ -Wall -o send send.cpp

#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
//#include <algorithm>
//#include <unistd.h>

//#define GOOGLECSV "/home/josh/.mutt/google.csv"
#define GOOGLECSV "/home/josh/Downloads/google.csv"

using namespace std;

int menu();

int main(int argc, char* argv[]) {

	int Continue = 1;
	string Search;
	vector<vector<string> > ContactsArrayFull;
	vector<int> resultsArray;
	string line;
	bool first=true;

	do{
		ifstream google(GOOGLECSV);
		if (!google) {
			cout << "Cannot open input file" << endl;
			return 1;
		}

		ContactsArrayFull.clear();
		resultsArray.clear();

		//Check if any arguements were given to program start and use these for
		//Search term. Else prompt for Search
		if ((argc < 2) || (first == false)) {
			cout << "Search: ";
			cin >> Search;
		}else{
			Search = argv[1];
		}

		//Until the end of the file, split each line into a vector, place each
		//line-vector into a global vector.
		int entryNumber=0;
		while(!google.eof()){
			getline(google,line);

			ContactsArrayFull.push_back(vector <string> ());

			string delimiter = ",";
			size_t pos = 0;
			string fieldContents;

			while ((pos = line.find(delimiter)) != string::npos) {
				fieldContents = line.substr(0, pos);

				ContactsArrayFull[entryNumber].push_back(fieldContents);
				line.erase(0, pos + delimiter.length());

			}
			entryNumber++;
		}

		int counter=0;
		int found = 0;
		cout << "Total size = " << ContactsArrayFull.size() << endl;
		cout << Search << endl;
		for (unsigned int i = 0; i < ContactsArrayFull.size()-1; ++i){

			for (unsigned int j = 0; j < ContactsArrayFull[i].size()-1; ++j){
				//string current = ContactsArrayFull[i][0];
				string current = ContactsArrayFull[i][j];
				if (current.find(Search, 0) != string::npos){
					cout << found << " " << ContactsArrayFull[i][0] << endl;
					++found;
					resultsArray.push_back(counter);
					break;
				}
			}
			++counter;
		}

		if (resultsArray.size() == 0){
			cout << "Search not found, please try again." << endl;
			google.clear();
			google.seekg(0);
		}else{
			int R;
			if (resultsArray.size() > 1){
				cout << "Choose a result: ";
				int pickResult;
				cin >> pickResult;
				R = resultsArray[pickResult];
			}else{
				R = resultsArray[0];
			}

			cout << endl;
			for (int i = 0; i < 83; ++i) {
				if (ContactsArrayFull[R][i] != ""){
					cout << left << setw(17) << ContactsArrayFull[0][i] << " = " << ContactsArrayFull[R][i] << endl;
				}
			}
			Continue = menu();
		}
		first = false;
		google.close();
	}while(Continue == 1);

}

int menu(){
	cout << endl;
	cout << "1 Search again\n"
		<< "0 Exit"
		<< endl;
	cout << "Choose an option: ";
	int option;
	cin >> option;

	return option;
}
