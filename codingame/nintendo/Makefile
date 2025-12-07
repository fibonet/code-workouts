CXX      := g++
CXXFLAGS := -std=c++23 -O2 -Wall -mpclmul -msse4.1

SRC := $(wildcard *.cpp)
EXE := $(basename $(SRC))

%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(EXE)
	./pgf2

clean:
	rm -f $(EXE)

