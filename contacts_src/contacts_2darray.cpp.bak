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

using namespace std;

int menu();
int countSubstring(const string& str, const string& sub);
bool startsWith(string str, string prefix);

int main(int argc, char* argv[]) {
string GOOGLECSV = "/home/josh/Downloads/google.csv";

	int Continue = 1;
	string Search;
	vector<vector<string> > ContactsArrayFull;
	vector<int> resultsArray;
	string line;
	bool first=true;
	ofstream testout("testout");

	do{
		ifstream google(GOOGLECSV.c_str());
		if (!google) {
			cout << "Cannot open input file" << endl;
			return 1;
		}

		string command = "iconv -f $(file -b --mime-encoding " + GOOGLECSV + ") -t UTF-8 " + GOOGLECSV + " > tmp"
							 /*+ " && tr '\r' ' ' <tmp > " + GOOGLECSV
							 + " && awk -F'\"' -v OFS='' '{ for (i=2; i<=NF; i+=2) gsub(\",\", \"\", $i) } 1' " + GOOGLECSV + " > tmp "*/
							 + " && mv tmp " + GOOGLECSV;
		system(command.c_str());

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

		/*----------------------------------------------------------------
		------------------ Contacts array generation ---------------------
		----------------------------------------------------------------*/
		//Until the end of the file, split each line into a vector, place each
		//line-vector into a global vector.
		int entryNumber=0;
		string line2;
		bool firstLine=true;
		string fieldsLine;

		while(!google.eof()){
			getline(google,line);

			//Get the number of fields from the number of commas in the first line
			if (firstLine){
				fieldsLine = line;
			}
			firstLine = false;

			//Deal with lines that are split by internal newlines
			while (countSubstring(line, ",") < countSubstring(fieldsLine, ",")){
				getline(google, line2);
				line = line + line2;
			}

			//Add new contact
			ContactsArrayFull.push_back(vector <string> ());

			string delimiter = ",";
			size_t pos = 0;
			string fieldContents;

			while ((pos = line.find(delimiter)) != string::npos) {
				fieldContents = line.substr(0, pos);

				//Add new field, and populate, to the new contact added above
				ContactsArrayFull[entryNumber].push_back(fieldContents);
				line.erase(0, pos + delimiter.length());

			}
			entryNumber++;
		}

		//Debuging - print out complete contact array
		for (unsigned int i = 0; i < ContactsArrayFull.size()-1; ++i){

			for (unsigned int j = 0; j < ContactsArrayFull[i].size()-1; ++j){
					testout << ContactsArrayFull[i][j] << "\t";
			}
			testout << endl;
		}

		/*----------------------------------------------------------------
		-------------------------- Search --------------------------------
		----------------------------------------------------------------*/
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
			//No results found
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
				//One result found
				R = resultsArray[0];
			}
			cout << endl;

			/*-----------------------------------------------------------
			-----------------Print to Screen ----------------------------
			-----------------------------------------------------------*/
			for (unsigned int i = 0; i < ContactsArrayFull[R].size(); ++i) {
				if (ContactsArrayFull[R][i] != ""){
					if (i < 27){
						//Standard info
						cout << left << setw(17) << ContactsArrayFull[0][i]
							<< " = " << ContactsArrayFull[R][i] << endl;
					}else if (startsWith(ContactsArrayFull[0][i], "E-mail")){
						//Emails
						cout << "Email " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else if (startsWith(ContactsArrayFull[0][i], "IM")){
						//IM
						cout << left << setw(17) << ContactsArrayFull[0][i]
							<< " = " << ContactsArrayFull[R][i] << endl;
					}else if (startsWith(ContactsArrayFull[0][i], "Phone")){
						//Phones
						cout << "Phone " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else if (startsWith(ContactsArrayFull[0][i], "Address")){
						//Address
					//	cout << left << setw(17) << ContactsArrayFull[0][i]
					//		<< " = " << ContactsArrayFull[R][i] << endl;
						cout << "Address " << ContactsArrayFull[R][i] << endl
								<< "        " << ContactsArrayFull[R][i+1] << endl
								<< "        " << ContactsArrayFull[R][i+2] << endl
								<< "        " << ContactsArrayFull[R][i+4] << endl
								<< "        " << ContactsArrayFull[R][i+5] << endl
								<< "        " << ContactsArrayFull[R][i+6] << endl
								<< "        " << ContactsArrayFull[R][i+7] << endl
								<< "        " << ContactsArrayFull[R][i+8] << endl;
						i=i+8;
					}else if (startsWith(ContactsArrayFull[0][i], "Organisation")){
						//Organisation
						cout << left << setw(17) << ContactsArrayFull[0][i]
							<< " = " << ContactsArrayFull[R][i] << endl;
					}else if (startsWith(ContactsArrayFull[0][i], "Relation")){
						//Relation
						cout << "Relation " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else if (startsWith(ContactsArrayFull[0][i], "Website")){
						//Website
						cout << "Website " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else if (startsWith(ContactsArrayFull[0][i], "Event")){
						//Event
						cout << "Event " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else if (startsWith(ContactsArrayFull[0][i], "Custom")){
						//Custom
						cout << "Event " << left << setw(11) << ContactsArrayFull[R][i]
							<< " = " << ContactsArrayFull[R][i+1] << endl;
						i++;
					}else{
						//Everything else
						cout << "Other " <<  left << setw(17) << ContactsArrayFull[0][i]
							<< " = " << ContactsArrayFull[R][i] << endl;
					}
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

/******************************************************************************
 *                                 Functions                                  *
 ******************************************************************************/

int countSubstring(const string& str, const string& sub)
{
    if (sub.length() == 0) return 0;
    int count = 0;
    for (size_t offset = str.find(sub); offset != string::npos;
	 offset = str.find(sub, offset + sub.length()))
    {
        ++count;
    }
    return count;
}

bool startsWith(string str, string prefix){
	if (str.compare(0, prefix.size(), prefix) == 0){
		return true;
	}else{
		return false;
	}
}
