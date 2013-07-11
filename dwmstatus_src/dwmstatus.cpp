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
#include <regex.h>

using namespace std;

/******************************************************************************
 *                                 Prototypes                                 *
 ******************************************************************************/
//the current unix time can be found using the command time(0).
string exec(string cmdstring);
bool testTimeNow(int duration, string prog, string arg);
string delLast(string str);

void open();
void mpd();
void mail();
void pac();

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

	pac();

	return 0;
}

/******************************************************************************
 *                                 Functions                                  *
 ******************************************************************************/
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

/******************************************************************************
 *                                   Items                                    *
 ******************************************************************************/
void open(){
	if (testTimeNow(300, "open", arg)) {
		string opn = exec("lsof | wc -l");
		ofstream openfile;
		openfile.open ("/tmp/dwm_status_bar/open");
		openfile << opn;
		openfile.close();
	}
}

void mpd(){
	//TODO convert from awk to c++
	string stat = exec("mpc status | awk 'NR==2 {print $1}'");

	string stat_short;
	if (stat == "[playing]\n") {
		stat_short="> ";
  	} else if (stat == "[paused]\n") {
		stat_short="|| ";
  	} else {
		stat_short="_ ";
  	}
	cout << stat_short << endl;

	string curMessy = exec("mpc current -f '[[%artist% - ]%title%]|[%file%]' | head -n 1");
	string cur = curMessy;
	string perc = exec("mpc | awk 'NR==2 {print $4}'");
	ofstream mpdfile;
	mpdfile.open("/tmp/dwm_status_bar/mpd");
	mpdfile << " \x08" << stat_short << delLast(perc) << " " << delLast(cur) << "\x01";
	mpdfile.close();
}

void mail(){
	if (testTimeNow(120, "email", arg)) {
		string feed = exec("nice -n 19 curl -n --silent 'https://mail.google.com/mail/feed/atom'");
	}
}

void pac(){
	if (testTimeNow(120, "pacman", arg)) {

		//TODO maybe count in c++ rather than spawning a wc shell.
		string pup = exec("pacman -Qqu | wc -l");
		pup = delLast(pup);

		ofstream pacfile;
		pacfile.open("/tmp/dwm_status_bar/pac");

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
