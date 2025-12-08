CXX      := g++
CXXFLAGS := -std=c++23 -O2 -Wall -mpclmul -msse4.1

SRC := $(wildcard *.cpp)
EXE := $(basename $(SRC))

%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
	./$@

.PHONY: clean
clean:
	rm -f $(EXE)

