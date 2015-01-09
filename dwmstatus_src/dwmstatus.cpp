//g++ -Wall -D{computer} -o send send.cpp

#include <iostream>
#include <cmath>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <sys/stat.h>
#include <sys/time.h>

#define TMP_FOLDER "/tmp/dwm_status_bar"
#define CURLMAIL

#if defined(LAPTOP)
#define INTERFACE  "wlan0"
#define DISKONE    "sda7"
#elif defined(DESKTOP)
#define INTERFACE  "wlp4s0"
#define DISKONE    "sda2"
#define DISKTWO    "sda3"
#define DISKTWOLAB "h"
#endif

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
int count(string str, char character);
string Get(const string & s, unsigned int n);

void open();
void mpd();
void mail();
void pac();
void hdd();
void ipa();
void net();
void date();

/******************************************************************************
 *                                    Main                                    *
 ******************************************************************************/
	string arg;
	struct timeval tval_before, tval_after, tval_result;
int main(int argc, char *argv[]) {

	if (argc == 1) {
		arg = "";
	} else {
		arg = argv[1];
	}

	gettimeofday(&tval_before, NULL);
	mpd();
	open();
	pac();
	mail();
	hdd();
	ipa();
	net();
	date();

	gettimeofday(&tval_after, NULL);
	timersub(&tval_after, &tval_before, &tval_result);
	printf("\t: %ld.%06ld\n", (long int)tval_result.tv_sec, (long int)tval_result.tv_usec);

	checkFolders();
	concatenate();
	popen("xsetroot -name \"$(cat /tmp/dwm_status_bar/content)\"", "r");

	return 0;
}

/******************************************************************************
 *                                 Functions                                  *
 ******************************************************************************/
/*
 * Check that the required temporary folder exists and, if it doesn't, create
 * it.
 */
void checkFolders() {
	struct stat st;
	if(stat(TMP_FOLDER,&st) == -1) {
		// if(st.st_mode & (S_IFDIR != 0))
		mkdir(TMP_FOLDER, 0777);
	}
}

/*
 * Open the output files for each of the functions, retreive their contents and
 * append them all to a single output file to be used as the contents of the
 * status bar. The order of the functions defined here determines the order of
 * the items in the bar.
 */
void concatenate() {
	int f = 8;
	string functions[f] = {"mpd", "open", "pac", "mail", "hdd", "ipa", "net", "dte"};

	ofstream out(TMP_FOLDER"/content");
	string line = "";
	for (int i = 0; i < f; i++) {
		stringstream filename;
		filename << TMP_FOLDER"/" << functions[i];
		ifstream in( filename.str().c_str() );
		while (getline(in, line)) {
			out << line;
		}
	}
	out << "  ";
}

/*
 * Interpret the given string as a shell command, run it and return the output
 * as a string.
 */
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

bool testTimeNow(int duration, string prog, string arg) {

	gettimeofday(&tval_after, NULL);
	timersub(&tval_after, &tval_before, &tval_result);
	printf("\t: %ld.%06ld\n", (long int)tval_result.tv_sec, (long int)tval_result.tv_usec);
	gettimeofday(&tval_before, NULL);

	if (duration == 0 || arg == "now") {
		cout << prog << "\t\t";
		return true;
	}
	int current = fmod(time(0),duration);
	cout << prog << "\t" << duration << "\t" << current;

	if (current > 0 && current < 11) {
		return true;
	} else {
		return false;
	}
}

/*
 * Remove the last character (often a newline character) from the end of a
 * string.
 */
string delLast(string str) {
	if (str.length() == 0) {
		return str;
	}
	return str.erase(str.length()-1);
}

/*
 * Returns the string that lies between the two deliminators, start_string and
 * end_string. eg substring("<p>this is as string</p>", "<p>", "</p>") would
 * return "this is a string".
 */
string substring(string text, string start_string, string end_string) {
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

/*
 * Return a count of the number of occurances of character in the string str.
 */
int count(string str, char character) {
	int count = 0;
	for (unsigned int i = 0; i < str.size(); ++i) {
		if (str[i] == character) {
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
/*
 * Number of open files used by the operating system and running programs, as
 * reported by lsof.
 */
void open() {
	if (testTimeNow(600, "open", arg)) {
		string opn = exec("lsof | wc -l");
		ofstream openfile;
		openfile.open (TMP_FOLDER"/open");
		openfile << "  " << opn;
		openfile.close();
	}
}

/*
 * The currently playing song from mpd with artist and playing percentage. If
 * no song is playing, or mpd is not running, then no output is created.
 */
void mpd() {
	testTimeNow(0, "mpd", arg);
	string mpcStatus = exec("mpc status 2> /dev/null");
	string stat = substring(mpcStatus, "[", "] ");

	string stat_short;
	string perc = "";
	string cur = "";
	if (stat != "") {
		if (stat == "playing") {
			stat_short="> ";
  		} else if (stat == "paused") {
			stat_short="|| ";
  		}

		//TODO implement cleaning of non printable characters
		string curMessy = exec("mpc current -f '[[%artist% - ]%title%]|[%file%]' 2> /dev/null| head -n 1");
		cur = delLast(curMessy);
		perc = substring(mpcStatus, "(", ")");
		perc = delLast(perc);
	}

	ofstream mpdfile;
	mpdfile.open(TMP_FOLDER"/mpd");
	mpdfile << "  \x08" << stat_short << perc << " " << cur << "\x01";
	mpdfile.close();
}

/*
 * Display the number of unread emails. Either use curl to get the value from
 * the gmail web feed (CURLMAIL) or count the number from the relevant folder
 * if an mbox directory is used (MBOXMAIL).
 */
void mail() {
	if (testTimeNow(120, "mail", arg)) {
		ofstream mailfile;
		mailfile.open(TMP_FOLDER"/mail");
#if defined(CURLMAIL)
		string feed = exec("nice -n 19 curl -n --silent 'https://mail.google.com/mail/feed/atom'");

		if (feed.find("fullcount") != string::npos) {
			string newNum = substring(feed, "<fullcount>", "</fullcount>");

			if (newNum != "0") {
				mailfile << "  \x04[M] \x01" << newNum;
			} else {
				mailfile << "";
			}
		} else {
			mailfile << "";
		}
#elif defined(MBOXMAIL)
		string number = exec("nice -n 19 find /home/josh/mail/gmail/INBOX/ -type f | grep -vE ',[^,]*S[^,]*$' | wc -l");
		number = delLast(number);

		if (number != "0") {
			mailfile << "  \x04[M] \x01" << number;
		} else {
			mailfile << "";
		}
#endif
		mailfile.close();
	}
}

/*
 * The number of availible updates as reported by pacman. This relies on an
 * update to the pacman database being performed at regular intervals
 * externally, eg via cron.
 */
void pac() {
	if (testTimeNow(120, "pman", arg)) {

		string pacup = exec("pacman -Qqu");
		int pup = count(pacup, '\n');

		ofstream pacfile;
		pacfile.open(TMP_FOLDER"/pac");

		if (pup != 0) {
			pacfile << "  \x04[P] \x01" << pup;
		} else {
			pacfile << "";
		}

		pacfile.close();
	}
}

/*
 * The percentage used of the hard disk paritions in use.
 */
void hdd() {
	if (testTimeNow(600, "hdd", arg)) {
		//TODO read from /proc to get hdd infor
		string disk1 = exec("df /dev/"DISKONE" --output=pcent | tail -n 1 | tr -d ' '");
#ifdef DISKTWO
		string disk2 = exec("df /dev/"DISKTWO" --output=pcent | tail -n 1 | tr -d ' '");
#endif
#ifdef DISKTHR
		string disk3 = exec("df /dev/"DISKTHR" --output=pcent | tail -n 1 | tr -d ' '");
#endif

		ofstream hddfile;
		hddfile.open(TMP_FOLDER"/hdd");
		hddfile << "  \x06[H] \x01/ " << delLast(disk1);
#if defined(DISKTWO) && defined(DISKTWOLAB)
		hddfile << " "DISKTWOLAB" " << delLast(disk2);
#endif
#if defined(DISKTHR) && defined(DISKTHRLAB)
		hddfile << " "DISKTHRLAB" " << delLast(disk3);
#endif
		hddfile.close();
	}
}

void ipa() {
	if (testTimeNow(3600, "ipa", arg)) {
		//TODO get wireless info
		///proc/net/tcp
		//use the second columnm, local_address, the ip address is here but in hex
		//and in reverse order. 0201A8C0 -> 192 168 1 2
		string ipcmd = "ip addr show dev "INTERFACE" | awk '/inet / {print $2}'";
		string ipaddr = exec(ipcmd);
		ipaddr = delLast(ipaddr);

		ofstream ipafile;
		ipafile.open(TMP_FOLDER"/ipa");
		ipafile << "  \x06[I] \x01" << ipaddr;
		ipafile.close();
	}
}

void net() {
	if (testTimeNow(600, "net", arg)) {

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
		} else {
			signal = signal_tmp + "%";
		}
		ofstream netfile;
		netfile.open(TMP_FOLDER"/net");
		netfile << "  \x06[W] \x01" << signal;
		netfile.close();
	}
}

void date() {
	testTimeNow(0, "date", arg);
	int seconds;
	ifstream uptimeFile("/proc/uptime");

	uptimeFile >> seconds;
	int minutes = seconds / 60 % 60;
	int hours = seconds / 60 / 60 % 24;
	int days = seconds / 60 / 60 / 24;

	ostringstream uptime;
	if (hours == 0) {
		uptime << minutes << "m ";
	} else if (days == 0) {
		uptime << hours << "h " << minutes << "m ";
	} else if (days > 10) {
		uptime << "\x03" << days << "d \x01" << hours << "h " << minutes << "m ";
	} else {
		uptime << days << "d " << hours << "h " << minutes << "m";
	}

	time_t t = time(0);   // get time now
	struct tm * now = localtime( & t );
	int year = now->tm_year - 100;
	int month = now->tm_mon + 1;
	int day = now->tm_mday;
	string month_long;
	switch(month) {
		case 1:  month_long = "Jan"; break;
		case 2:  month_long = "Feb"; break;
		case 3:  month_long = "Mar"; break;
		case 4:  month_long = "Apr"; break;
		case 5:  month_long = "May"; break;
		case 6:  month_long = "Jun"; break;
		case 7:  month_long = "Jul"; break;
		case 8:  month_long = "Aug"; break;
		case 9:  month_long = "Sep"; break;
		case 10: month_long = "Oct"; break;
		case 11: month_long = "Nov"; break;
		case 12: month_long = "Dec"; break;
		default: month_long = "Unk"; break;
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
	} else {
		ampm = "am";
	}

	ostringstream minPad;
	if (minute < 10) {
		minPad << "0" << minute;
	} else {
		minPad << minute;
	}
	ostringstream secPad;
	if (second < 10) {
		secPad << "0" << second;
	} else {
		secPad << second;
	}

	ostringstream timeNow;
	timeNow << hour << ":" << minPad.str() << ":" << secPad.str() << ampm;

	ofstream datefile;
	datefile.open(TMP_FOLDER"/dte");
	datefile << "  \x06[Up] \x01" << uptime.str() << "   \x08" << timeNow.str() << "\x01   " << dateNow.str();
	datefile.close();
}
