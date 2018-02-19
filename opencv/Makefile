
### bash profile
### export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

version:version.cpp
	g++ -o $@.o  $< `pkg-config --libs opencv` `pkg-config --cflags opencv` ;./$@.o
capture:capture.cpp
	g++ -o $@.o  $< `pkg-config --libs opencv` `pkg-config --cflags opencv` ;./$@.o
