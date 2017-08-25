#include <stdio.h>

static void cksum(FILE *fp, const char *s) {
	printf("Hello");
	printf(s);
}

int main (int argc, char *argv[]) {
	if (argc != 2) {
		printf("usage: %s filename", argv[0]);
	} else {
		FILE *file = fopen(argv[1], "r");
		
		if ( file == 0 ) {
			printf("Could not open file\n");
		} else {
			int x;
			long int tot = 0;
			while ((x = fgetc(file)) != EOF) {
				tot ^= x;
			}
			fclose( file );
			printf("%i\n", tot);
		}
	}
}