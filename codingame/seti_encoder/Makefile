CXX      := g++
CXXFLAGS := -std=c++23 -O2 -Wall

SRC := $(wildcard *.cpp)
EXE := $(basename $(SRC))

%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

run: $(EXE)
	echo "here on run $(EXE)"
	./nintendo < input.txt

clean:
	rm -f $(EXE)

