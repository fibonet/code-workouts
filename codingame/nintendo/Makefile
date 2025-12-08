CXX      := g++
CXXFLAGS :=-MMD -MP -std=c++23 -O2 -Wall -mpclmul -msse4.1

HEADERS := $(wildcard *.h)
SOURCES := $(wildcard *.cpp)
EXES := $(SOURCES:.cpp=)
DEPENDS := $(SOURCES:.cpp=.d)
MAIN := work-pgf2-64
READ ?= ./032-input.txt


%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

-include $(DEPENDS)

.PHONY: all clean run

all: $(MAIN)

run: $(MAIN)
	./$(MAIN) < $(READ)

clean:
	rm -f $(EXES) $(DEPENDS)

