#
# Makefile for 'contacts'.
#
# Type 'make' or 'make contacts' to create the executable.
# Type 'make clean' to delete all temporaries.
#

CC = g++

# build target specs
CFLAGS = -g -Wall -DDEBUG
OUT_DIR = debug_build
LIBS =

# first target entry is the target invoked when typing 'make'
default: contacts

contacts: $(OUT_DIR)/contacts_CharRead.cpp.o
	$(CC) $(CFLAGS) -o contacts $(OUT_DIR)/contacts_CharRead.cpp.o $(LIBS)

$(OUT_DIR)/contacts_CharRead.cpp.o: contacts_CharRead.cpp
	$(CC) $(CFLAGS) -o $(OUT_DIR)/contacts_CharRead.cpp.o -c contacts_CharRead.cpp

clean:
	rm -f contacts $(OUT_DIR)/*.o

profile:
	gprof contacts > profile.txt; ./gprof2dot.py profile.txt | dot -Tpng -o profile.png
