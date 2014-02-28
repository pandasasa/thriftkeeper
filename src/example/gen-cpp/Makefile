LIB_DIR = ../../lib/cpp

CXXFLAGS = -Wall

INC = -I${HOME}/include -I/usr/local/include -I${LIB_DIR}

LIB = -L${HOME}/lib -lzookeeper_mt -ljson -L/usr/lib/ -lgflags -L/usr/local/lib -lthrift

SRC = ${wildcard *.cpp} ${wildcard ${LIB_DIR}/*.cpp}

OBJ = ${patsubst %.cpp,%.o,${SRC}}

TARGET = Calculator_server SharedService_server

.PHONY: all clean

all: ${TARGET}

%.o: %.cpp
	${CXX} ${CXXFLAGS} ${INC} -c $< -o $@

Calculator_server: ${patsubst SharedService_server.o,,${OBJ}}
	${CXX} $^ ${LIB} -o $@

SharedService_server: ${patsubst Calculator_server.o,,${OBJ}}
	${CXX} $^ ${LIB} -o $@

clean:
	${RM} ${OBJ}
	