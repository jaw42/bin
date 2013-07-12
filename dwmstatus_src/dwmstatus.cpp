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
	string output = str.erase(str.length()-1);
	return output;
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
	return 0;
}

/******************************************************************************
 *                                   Items                                    *
 ******************************************************************************/
void open(){
	if (testTimeNow(300, "open", arg)) {
		string opn = exec("lsof | wc -l");
		ofstream openfile;
		openfile.open (TMP_FOLDER"/open");
		openfile << " " << opn;
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
	mpdfile << " \x08" << stat_short << delLast(perc) << " " << delLast(cur) << "\x01";
	mpdfile.close();
}

void mail(){
	if (testTimeNow(120, "email", arg)) {
		string feed = exec("nice -n 19 curl -n --silent 'https://mail.google.com/mail/feed/atom'");
		string newNo = substring(feed, "<fullcount>", "</fullcount>");

		ofstream mailfile;
		mailfile.open(TMP_FOLDER"/mail");
		if (newNo != "0") {
			mailfile << " \x04M:\x01" << newNo;
		}else{
			mailfile << "";
		}
		mailfile.close();
	}
}

void pac(){
	if (testTimeNow(120, "pacman", arg)) {

		//TODO maybe count in c++ rather than spawning a wc shell.
		string pup = exec("pacman -Qqu | wc -l");
		pup = delLast(pup);

		ofstream pacfile;
		pacfile.open(TMP_FOLDER"/pac");

		if (pup != "0") {

			//TODO create a notify-send function to make this easier.
			string message = "notify-send 'pacman has been run (" + pup + " updates)'";
			popen(message.c_str(),"r");
			pacfile << " \x04P:\x01" << pup;
		}else{
			pacfile << "";
		}

		pacfile.close();
	}
}

void hdd(){
	//TODO read from /proc to get hdd infor
	string disk = exec("df /dev/sda7 --output=pcent | tail -n 1 | tr -d ' '");
	ofstream hddfile;
	hddfile.open(TMP_FOLDER"/hdd");
	hddfile << " \x06H:\x01" << delLast(disk);
	hddfile.close();
}

void net(){
	//TODO get wireless info
	///proc/net/tcp
	//use the second columnm, local_address, the ip address is here but in hex
	//and in reverse order. 0201A8C0 -> 192 168 1 2
	string ipaddr=exec("ifconfig wlan0 | awk '/inet / {print $2}'");
	ipaddr = delLast(ipaddr);
	string signal_tmp=exec("cat /proc/net/wireless | grep wlan0 | awk '{print $3}' | tr -d '.'");
	signal_tmp = delLast(signal_tmp);

	int signal_int;
	stringstream(signal_tmp) >> signal_int;

	string signal;
	if (signal_int < 30) {
		signal = "\x07" + signal_tmp + "%\x01";
	}else{
		signal = signal_tmp + "%";
	}
	ofstream netfile;
	netfile.open(TMP_FOLDER"/net");
	netfile << " \x06I:\x01(" << ipaddr << ") \x06W:\x01" << signal;
	netfile.close();

}

void date(){
	//TODO read from /proc/uptime to get uptime info
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
	//TODO pad minutes so its always 2 characters wide.
	int minute = now->tm_min;
	int second = now->tm_sec;
	string ampm;
	if (hour > 12) {
		hour = hour - 12;
		ampm = "pm";
	}else{
		ampm = "am";
	}
	ostringstream timeNow;
	timeNow << hour << ":" << minute << ":" << second << ampm;

	ofstream datefile;
	datefile.open(TMP_FOLDER"/dte");
	datefile << " \x06Up:\x01" << uptime.str() << " \x08" << timeNow.str() << "\x01 " << " " << dateNow.str();
	datefile.close();
}
