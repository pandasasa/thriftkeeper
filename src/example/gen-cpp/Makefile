LIB_DIR = ../../lib/cpp

CXXFLAGS = -Wall

INC = -I/usr/include/curl -I/usr/include/openssl -I/usr/include/boost -I/usr/local/include \
	-I/usr/local/include/thrift -I${HOME}/zookeeper/include -I${LIB_DIR}

LIB = -L/usr/lib/ -lgflags -L/usr/local/lib -lthrift -L${HOME}/zookeeper/lib -lzookeeper_mt

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
	