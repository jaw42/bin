//g++ -Wall -o send send.cpp

#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>

using namespace std;

bool verbose=false;

int menu();
int countSubstring(const string& str, const string& sub);
bool startsWith(string str, string prefix);

int main(int argc, char* argv[]) {
	//string GOOGLECSV = "/home/josh/Downloads/google.csv";
	string GOOGLECSV = "/home/josh/.mutt/google.csv";

	string command = "iconv -f $(file -b --mime-encoding " + GOOGLECSV + ") -t UTF-8 " + GOOGLECSV + " > /tmp/google"
						 		+ " && mv /tmp/google " + GOOGLECSV;
	system(command.c_str());

	ifstream google(GOOGLECSV.c_str());
	if (!google) {
		cout << "Cannot open input file" << endl;
		return 1;
	}


	vector<vector<string> > ContactsArrayFull;
	ContactsArrayFull.push_back(vector <string> ());

	/*----------------------------------------------------------------
	------------------ Contacts array generation ---------------------
	----------------------------------------------------------------*/
	int entryNumber = 0;
	double fieldNumber = 0;
	string fieldsLine;

	getline(google,fieldsLine);
	int totalFields = countSubstring(fieldsLine, ",");
	google.clear();
	google.seekg(0);

	string currentField;
	bool insideQuote = false;
	char c;

	//Ignore first three escape characters
	c = google.get();
	c = google.get();
	c = google.get();
	while(google){

		c = google.get();
		if ((c == '"') && (insideQuote == false)){
			insideQuote = true;
		}else if((c == '"') && (insideQuote == true)){
			insideQuote = false;
		}

		if ((c == ',') && (insideQuote == false)){
			fieldNumber++;
			//cout << currentField << endl;

			ContactsArrayFull[entryNumber].push_back(currentField);
			currentField = "";
		//}else if((c != '\n') && (c != '\r') && (c != '"')){
		}else if((c == '\n') || (c == '\r')){
			currentField += c;
			currentField += ' ';
		}else if((c != '\n') && (c != '\r')){
			currentField += c;
		}

		if ((fieldNumber == totalFields) && (c == '\n')){
			ContactsArrayFull.push_back(vector <string> ());
			entryNumber++;
			fieldNumber = 0;
		}
	}

	//Debuging - print out complete contact array
	if(verbose){
		ofstream testout("testout");
		for (unsigned int i = 0; i < ContactsArrayFull.size()-1; ++i){

			for (unsigned int j = 0; j < ContactsArrayFull[i].size()-1; ++j){
					testout << ContactsArrayFull[i][j] << "\t";
			}
			testout << endl;
		}
	}

	/*----------------------------------------------------------------
	-------------------------- Search --------------------------------
	----------------------------------------------------------------*/
	int Continue = 1;
	string Search;
	vector<int> resultsArray;
	bool first=true;
	do{
		//Check if any arguements were given to program start and use these for
		//Search term. Else prompt for Search
		if ((argc < 2) || (first == false)) {
			cout << "Search: ";
			cin >> Search;
		}else{
			Search = argv[1];
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
				cout << "Something"  << endl;

		if (resultsArray.size() == 0){
			//No results found
			cout << "Search not found, please try again." << endl;
			google.clear();
			google.seekg(0);
		}else{
			int R;
			if (resultsArray.size() > 1){
				cout << "Choose a result: ";
				unsigned int pickResult;
				cin >> pickResult;

				while ((cin.fail()) || (pickResult < 0) || pickResult > resultsArray.size()){
					cout << "Not a valid selection. Choose a result: ";
					cin >> pickResult;
				}
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
						cout << "Address " << ContactsArrayFull[R][i] << endl;
						int q[] = {1,2,8,3,4,5,6,7};
						for (int p = 0; p < 8; ++p) {
							if (ContactsArrayFull[R][i+q[p]] != ""){
								cout << p << setw(17) << "        " << ContactsArrayFull[R][i+q[p]] << endl;
							}
						}
								/*<< " 2      " << ContactsArrayFull[R][i+2] << endl
								<< " 7      " << ContactsArrayFull[R][i+8] << endl
								<< " 3      " << ContactsArrayFull[R][i+4] << endl
								<< " 4      " << ContactsArrayFull[R][i+5] << endl
								<< " 5      " << ContactsArrayFull[R][i+6] << endl
								<< " 6      " << ContactsArrayFull[R][i+7] << endl;*/
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
			Continue = 0;
			Continue = menu();
			if (Continue == 1){
				Search = "";
			}
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
