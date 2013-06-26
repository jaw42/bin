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

#define ADDRESSBOOK "/home/josh/.mutt/aliases"

using namespace std;

string split(string StringToSplit, string Separators, int position);
string splitToNames(string everything);

// used for max_element to get the longest something.
// takes two arguements and returns whether the first is bigger than second
struct length {
    bool operator() ( const string& a, const string& b ){
        return a.size() < b.size();
    }
};

int main(int argc, char* argv[]) {
    string search;
    
    ifstream contacts (ADDRESSBOOK);

    if (!contacts) {
        cout << "Cannot open input file" << endl;
        return 1;
    }
    
    vector<string> emailArray;
    vector<string> nameArray;
    string line;
    unsigned int offset;
    bool first=true;

    do{
        if ((argc < 2) || (first == false)) {
            cout << "Search: ";
            cin >> search;
        }else{
            search = argv[1];
        }

        while(!contacts.eof()){
            getline(contacts,line);
            if ((offset = line.find(search, 0)) != string::npos) {
                string name;
                name = split(line, "<", 1);
                name = splitToNames(name);
                nameArray.push_back(name);

                string email;
                email = split(line, "<", 2);
                email = email.substr(0, email.size()-1);

                emailArray.push_back(email);
            }
        }

        contacts.close();

        unsigned int pos;
        
        string longest;
        longest = *max_element(nameArray.begin(), nameArray.end(), length());
        int longestLength = longest.size();

        int Number = emailArray.size();
        string String = static_cast<ostringstream*>( &(ostringstream() << Number) )->str();

        for (pos = 0; pos < emailArray.size(); pos++) {
            cout << setw(String.size()) << pos << " " 
                << setw(longestLength) << nameArray[pos] << "  " 
                << emailArray[pos] << endl;
        }
        first=false;

    }while(emailArray.size() == 0);
    
    unsigned int select = 0;

    if (emailArray.size() == 1) {
        cout << "Do the next thing, there was only one entry found" << endl;
    }else{
        cout << "Choose: ";
        cin >> select;
        while((select > emailArray.size())){
            cout << "Not valid, choose: ";
            cin >> select;
        }
    }
    cout << "\n\n\n" << emailArray[select] << endl;
    string Choice = emailArray[select];
    execlp("mailx", "-A gmail", Choice.c_str(), (char *)NULL);

    return 0;
}

// Functions --------------------------------------------------------------

string split(string StringToSplit, string Separators, int position) {

    size_t EndPart1 = StringToSplit.find_first_of(Separators);
    string Part1 = StringToSplit.substr(0, EndPart1);
    string Part2 = StringToSplit.substr(EndPart1 + 1);

    if (position == 1) {
        return Part1;
    }else{
        return Part2;
    }
}

string splitToNames(string everything) {
    stringstream ss(everything);
    string s, finalName;
    vector<string> justName;

    while (getline(ss, s, ' ')) {
        justName.push_back(s);
    }
    justName.erase(justName.begin(),justName.begin()+2);

    unsigned int i;
    for (i = 0; i < justName.size(); i++) {
        finalName += justName[i];
        finalName += " ";
    }
//    cout << "final name = " << finalName << endl;
    return finalName;
}
