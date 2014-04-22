//g++ -Wall -o send send.cpp

#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>
#include <math.h>
#include <algorithm>
#include <fstream>
#include <stdio.h>
#include <ctime>
#include <sstream>
#include <sys/stat.h>

#define TMP_FOLDER "/tmp/dwm_status_bar"
#define INTERFACE "wlan0"

using namespace std;

/******************************************************************************
 *                                 Prototypes                                 *
 ******************************************************************************/
//the current unix time can be found using the command time(0).
void checkFolders();

string exec(string cmdstring);
bool testTimeNow(int duration, string prog, string arg);
string delLast(string str);
string substring(string text, string start_string, string end_string);
void concatenate();
int count(string String, char character);
string Get(const string & s, unsigned int n);

void open();
void mpd();
void mail();
void pac();
void hdd();
void net();
void date();

/******************************************************************************
 *                                    Main                                    *
 ******************************************************************************/
	string arg;
int main(int argc, char *argv[]){

	if (argc == 1) {
		arg = "";
	}else{
		arg = argv[1];
	}

	mpd();
	open();
	pac();
	mail();
	hdd();
	net();
	date();
	checkFolders();
	concatenate();
	popen("xsetroot -name \"$(cat /tmp/dwm_status_bar/content)\"", "r");

	return 0;
}

/******************************************************************************
 *                                 Functions                                  *
 ******************************************************************************/
void checkFolders(){
	struct stat st;
	if(stat(TMP_FOLDER,&st) == -1){
		//	if(st.st_mode & (S_IFDIR != 0))
		mkdir(TMP_FOLDER, 0777);
	}
}

void concatenate(){
	string functions[7] = {"mpd", "open", "pac", "mail", "hdd", "net", "dte"};

	ofstream out(TMP_FOLDER"/content");
	string line = "";
	for (int i = 0; i < 7; i++) {
		stringstream filename;
		filename << TMP_FOLDER << "/" << functions[i];
		ifstream in( filename.str().c_str() );
		while (getline(in, line)) {
			out << line;
		}
	}
	out << "  ";
}

string exec(string cmdstring) {
	char* cmd = (char*)cmdstring.c_str();
	FILE* pipe = popen(cmd, "r");
	if (!pipe) return "ERROR";
	char buffer[128];
	string result = "";
	while(!feof(pipe)) {
		if(fgets(buffer, 128, pipe) != NULL)
			result += buffer;
	}
	pclose(pipe);
	return result;
}

bool testTimeNow(int duration, string prog, string arg){

	if (arg == "now") {
		return true;
	}
	int current = fmod(time(0),duration);
	cout << prog << "\t" << duration << "\t" << current << endl;

	if (current > 0 && current < 11) {
		return true;
	}else{
		return false;
	}
}

string delLast(string str){
	return str.erase(str.length()-1);
}

string substring(string text, string start_string, string end_string){
//Returns the string that lies between the two deliminators, start_string and
//end_string. eg substring("<p>this is as string is this</p>", "<p>", "</p>") would
//return "this is a string is this".
	string::size_type start_pos = 0;
	string::size_type end_pos = 0;
	string found_text;

	start_pos = text.find(start_string);
	if (start_pos != std::string::npos) {
		++start_pos; // start after the double quotes.

		// look for end position;
		end_pos = text.find(end_string);
		if (end_pos != std::string::npos) {
			found_text = text.substr(start_pos+start_string.size()-1, end_pos-start_pos-end_string.size()+2);
			return found_text;
		}
	}
	return " ";
}

int count(string String, char character){
	int count = 0;
	for (unsigned int i = 0; i < String.size(); ++i) {
		if (String[i] == character) {
			count++;
		}
	}
	return count;
}

string Get(const string & s, unsigned int n) {
    istringstream is( s );
    string field;
    do {
        if ( ! ( is >> field ) ) {
            return "";
        }
    } while( n-- != 0 );
    return field;
}

/******************************************************************************
 *                                   Items                                    *
 ******************************************************************************/
void open(){
	if (testTimeNow(300, "open", arg)) {
		string opn = exec("lsof | wc -l");
		ofstream openfile;
		openfile.open (TMP_FOLDER"/open");
		openfile << "  " << opn;
		openfile.close();
	}
}

void mpd(){
	string mpcStatus = exec("mpc status");
	string stat = substring(mpcStatus, "[", "] ");

	string stat_short;
	if (stat == "playing") {
		stat_short="> ";
  	} else if (stat == "paused") {
		stat_short="|| ";
  	} else {
		stat_short="_ ";
  	}

	//TODO implement cleaning of non printable characters
	string curMessy = exec("mpc current -f '[[%artist% - ]%title%]|[%file%]' | head -n 1");
	if (curMessy == "") {
		curMessy = " ";
	}
	string cur = curMessy;
	string perc = substring(mpcStatus, "(", ")");

	ofstream mpdfile;
	mpdfile.open(TMP_FOLDER"/mpd");
	mpdfile << "  \x08" << stat_short << delLast(perc) << " " << delLast(cur) << "\x01";
	mpdfile.close();
}

void mail(){
	if (testTimeNow(120, "email", arg)) {
		string feed = exec("nice -n 19 curl -n --silent 'https://mail.google.com/mail/feed/atom'");

		ofstream mailfile;
		mailfile.open(TMP_FOLDER"/mail");
		if (feed.find("fullcount") != string::npos) {
			string newNo = substring(feed, "<fullcount>", "</fullcount>");

			if (newNo != "0") {
				mailfile << "  \x04[M] \x01" << newNo;
			}else{
				mailfile << "";
			}
		}else{
			mailfile << "";
		}
		mailfile.close();
	}
}

void pac(){
	if (testTimeNow(120, "pacman", arg)) {

		string pacup = exec("pacman -Qqu");
		int pup = count(pacup, '\n');

		ofstream pacfile;
		pacfile.open(TMP_FOLDER"/pac");

		if (pup != 0) {
			pacfile << "  \x04[P] \x01" << pup;
		}else{
			pacfile << "";
		}

		pacfile.close();
	}
}

void hdd(){
	//TODO read from /proc to get hdd infor
	string disk = exec("df /dev/sda3 --output=pcent | tail -n 1 | tr -d ' '");
	ofstream hddfile;
	hddfile.open(TMP_FOLDER"/hdd");
	hddfile << "  \x06[H] \x01" << delLast(disk);
	hddfile.close();
}

void net(){
	//TODO get wireless info
	///proc/net/tcp
	//use the second columnm, local_address, the ip address is here but in hex
	//and in reverse order. 0201A8C0 -> 192 168 1 2
	string ipaddr=exec("ip addr show dev wlan0 | awk '/inet / {print $2}'");
	if (ipaddr != "") {
		ipaddr = delLast(ipaddr);
	}
	string signal_tmp;

	ifstream wireless("/proc/net/wireless");
	while (getline(wireless, signal_tmp)) {
		if (signal_tmp.find(INTERFACE) != string::npos) {
		signal_tmp = Get(signal_tmp, 2);
			signal_tmp = delLast(signal_tmp);
			break;
		}
	}

	int signal_int;

	signal_int = atoi(signal_tmp.c_str());

	string signal;
	if (signal_int < 30) {
		signal = "\x07" + signal_tmp + "%\x01";
	}else{
		signal = signal_tmp + "%";
	}
	ofstream netfile;
	netfile.open(TMP_FOLDER"/net");
	netfile << "  \x06[I] \x01(" << ipaddr << ")  \x06[W] \x01" << signal;
	netfile.close();

}

void date(){
	int seconds;
	ifstream uptimeFile("/proc/uptime");

	uptimeFile >> seconds;
	int minutes = seconds / 60 % 60;
	int hours = seconds / 60 / 60 % 24;
	int days = seconds / 60 / 60 / 24;

	ostringstream uptime;
	if (days == 0) {
		uptime << hours << "h " << minutes << "m ";
	}else if (days > 7) {
		uptime << "\x03" << days << "d \x01" << hours << "h " << minutes << "m ";
	}else{
		uptime << days << "d " << hours << "h " << minutes << "m";
	}

	time_t t = time(0);   // get time now
	struct tm * now = localtime( & t );
	int year = now->tm_year - 100;
	int month = now->tm_mon + 1;
	int day = now->tm_mday;
	string month_long;
	switch(month){
		case 1: month_long = "Jan"; break;
		case 2: month_long = "Feb"; break;
		case 3: month_long = "Mar"; break;
		case 4: month_long = "Apr"; break;
		case 5: month_long = "May"; break;
		case 6: month_long = "Jun"; break;
		case 7: month_long = "Jul"; break;
		case 8: month_long = "Aug"; break;
		case 9: month_long = "Sep"; break;
		case 10: month_long = "Oct"; break;
		case 11: month_long = "Nov"; break;
		case 12: month_long = "Dec"; break;
		default: month_long = "Unknown"; break;
	}
	ostringstream dateNow;
	dateNow << day << " " << month_long << "'" << year;

	int hour = now->tm_hour;
	int minute = now->tm_min;
	int second = now->tm_sec;
	string ampm;
	if (hour > 12) {
		hour = hour - 12;
		ampm = "pm";
	}else{
		ampm = "am";
	}

	ostringstream minPad;
	if (minute < 10) {
		minPad << "0" << minute;
	}else{
		minPad << minute;
	}
	ostringstream secPad;
	if (second < 10) {
		secPad << "0" << second;
	}else{
		secPad << second;
	}

	ostringstream timeNow;
	timeNow << hour << ":" << minPad.str() << ":" << secPad.str() << ampm;

	ofstream datefile;
	datefile.open(TMP_FOLDER"/dte");
	datefile << "  \x06[Up] \x01" << uptime.str() << "   \x08" << timeNow.str() << "\x01   " << dateNow.str();
	datefile.close();
}
