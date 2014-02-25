CXXFLAGS := -Wall

INC := -I/usr/include/curl -I/usr/include/openssl -I/usr/include/boost -I/usr/local/include/thrift \
	-I/usr/local/include

LIB := -L/usr/lib/ -lcurl -lssl -lm -L/usr/local/lib -lthrift

GEN_RC = Calculator.cpp shared_constants.cpp shared_types.cpp SharedService.cpp \
	tutorial_constants.cpp tutorial_types.cpp

GEN_OBJ = $(patsubst %.cpp,%.o, $(GEN_RC))

TARGET = Calculator_server SharedService_server

.PHONY: all clean

all: $(TARGET)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INC) -c $< -o $@

Calculator_server: Calculator_server.o $(GEN_OBJ)
	$(CXX) $^ -o $@ $(LIB)

SharedService_server: SharedService_server.o $(GEN_OBJ)
	$(CXX) $^ -o $@ $(LIB)

clean:
	$(RM) *.o $(TARGET)
	