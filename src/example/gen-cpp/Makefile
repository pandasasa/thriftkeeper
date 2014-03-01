LIB_DIR = ../../lib/c

CXXFLAGS = -Wall

INC = -I/usr/local/include -I${LIB_DIR}

LIB = -L/usr/lib/ -lgflags -L/usr/local/lib -lthrift -lzookeeper_mt -ljson-c

SRC = ${wildcard *.cpp} ${wildcard ${LIB_DIR}/*.c}

OBJ = ${patsubst %.cpp,%.o,${patsubst %.c,%.o,${SRC}}}

TARGET = Calculator_server SharedService_server

.PHONY: all clean

all: ${TARGET}

%.o: %.cpp
	${CXX} ${CXXFLAGS} ${INC} -c $< -o $@

%.o: %.c
	${CXX} ${CXXFLAGS} ${INC} -c $< -o $@

Calculator_server: ${patsubst SharedService_server.o,,${OBJ}}
	${CXX} $^ ${LIB} -o $@

SharedService_server: ${patsubst Calculator_server.o,,${OBJ}}
	${CXX} $^ ${LIB} -o $@

clean:
	${RM} ${OBJ}
	