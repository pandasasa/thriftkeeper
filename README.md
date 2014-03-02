# Thriftkeeper

## Introduction

Thriftkeeper is a library, which can be used in thrift server and client program to make a highly reliable rpc service. The key features it supported are load balancing, auto scaling, auto fail over, service monitoring and managing.

It uses [thrift][thrift] as the rpc framework, and [zookeeper][zookeeper] as the distributed coordination. As thrift is a cross language rpc framework, so naturally it supports multi languages, right now including c/c++, python and php. 

## Features

*  client load balancing, the balancing algorithms including random, round robin, by weight, least connections.
*  auto scaling, to add new rpc server, the only thing you need to do is start the server, client will know the new server automatically.
*  auto fail over, if a rpc server down, client will be noticed in few seconds, and no new calling will send to this server.
*  monitoring and managing, current servers and clients online, connections on each server, number of callings received by each server etc, everything you want to know can found on the web admin console.

## Usage

### Directory structure

The server api using example is in "src/example/gen-cpp/Calculator_server.cpp", and the client api using example is in "src/example/gen-py/client.py".

<pre>
.
├── LICENSE
├── README.md
└── src
    ├── example
    │   ├── gen-cpp
    │   │   ├── Calculator.cpp
    │   │   ├── Calculator.h
    │   │   ├── Calculator_server
    │   │   ├── Calculator_server.cpp
    │   │   ├── Makefile
    │   │   ├── SharedService.cpp
    │   │   ├── SharedService.h
    │   │   ├── SharedService_server
    │   │   ├── SharedService_server.cpp
    │   │   ├── shared_constants.cpp
    │   │   ├── shared_constants.h
    │   │   ├── shared_types.cpp
    │   │   ├── shared_types.h
    │   │   ├── tutorial_constants.cpp
    │   │   ├── tutorial_constants.h
    │   │   ├── tutorial_types.cpp
    │   │   └── tutorial_types.h
    │   ├── gen-php
    │   ├── gen-py
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── shared
    │   │   └── tutorial
    │   ├── shared.thrift
    │   └── tutorial.thrift
    └── lib
        ├── c
        │   ├── thriftkeeper.c
        │   └── thriftkeeper.h
        ├── php
        └── python
            ├── thriftkeeper.py
</pre>

### Runing results

 1. prerequisite

    Install [thrift][thrift] and [zookeeper][zookeeper].
    
 1. start zookeeper service in cluster mode

    Start zookeeper service in cluster mode, we started three instances on one machine. Suppose zookeeper installed to your home directory, and  "zoo1.cfg", "zoo2.cfg" and "zoo3.cfg" are config files under  "~/zookeeper/conf".

    <pre>
    > cd ~/zookeeper
    > ./bin/zkServer.sh start zoo1.cfg
    > ./bin/zkServer.sh start zoo2.cfg
    > ./bin/zkServer.sh start zoo2.cfg
    </pre>
    
 1. start rpc server

    Before start, you need to compile first. Make sure you already installed this libraries, including [gflags][gflags], [json-c][json-c] and of course, thrift and zookeeper. The makefile suppose that all the header files installed in "/usr/local/include", gflags lib in "/usr/lib", and other libs in "/usr/local/lib", modify it as your situation.
    
    Go into "src/example/gen-cpp" and run "make" command, if everything ok, you will get the server program "Calculator_server". Start three instances listening at different port and with different node name.

    <pre>
    > cd src/example/gen-cpp
    > make
    > ./Calculator_server --help
    > ./Calculator_server -port=9091 -zk_node_name=node1 ~/data/thriftkeeper/tutorial_node1.log 2>&1 &
    > ./Calculator_server -port=9092 -zk_node_name=node2 ~/data/thriftkeeper/tutorial_node1.log 2>&1 &
    > ./Calculator_server -port=9093 -zk_node_name=node4 ~/data/thriftkeeper/tutorial_node1.log 2>&1 &
    </pre>
    
    When starting server, it will firstly register itself on zookeeper as a children of node "/thriftkeeper/tutorial/providers", along with its service address. It will try to register itself again if connection lost, and the node on zookeeper which represent itself will be deleted when server stopped.

 1. run client
 
    Run client script, give procedure argument as "ping", it will continuously call remote procedure "ping".

    When starting client, it will firstly register itself on zookeeper as a children of node "/thriftkeeper/tutorial/consumers", get all servers that are online, then choose one server by random and call remote procedure continuely. 

    <pre>
    > cd src/example/gen-py
    > ./client.py -h
    > ./client.py ping
    notification received, type - -1, state - 3, path -
    register succeed
    called procedure ping 1 times
    called procedure ping 2 times
    called procedure ping 3 times
    called procedure ping 4 times
    called procedure ping 5 times
    called procedure ping 6 times
    </pre>
    
    When new server added or some online server down, it will be notified immediately.
 
    <pre>   
    provider address, host - 127.0.0.1, port - 9091
    called procedure ping 3 times
    provider address, host - 127.0.0.1, port - 9093
    called procedure ping 4 times
    provider address, host - 127.0.0.1, port - 9091
    called procedure ping 5 times
    provider address, host - 127.0.0.1, port - 9092
    called procedure ping 6 times
    ...
    // here we stopped server1, it will be no more calling to server1
    provider node1 changed, type - 2, state - 3, path - /thriftkeeper/tutorial/providers/node1
    providers changed, type - 4, state - 3, path - /thriftkeeper/tutorial/providers
    provider address, host - 127.0.0.1, port - 9093
    called procedure ping 10 times
    provider address, host - 127.0.0.1, port - 9093
    called procedure ping 11 times
    provider address, host - 127.0.0.1, port - 9092
    called procedure ping 12 times
    provider address, host - 127.0.0.1, port - 9092
    ...
    // here we restarted server1, calling to server1 will appear again
    providers changed, type - 4, state - 3, path - /thriftkeeper/tutorial/providers
    provider address, host - 127.0.0.1, port - 9091
    called procedure ping 19 times
    provider address, host - 127.0.0.1, port - 9093
    called procedure ping 20 times
    ...
    provider address, host - 127.0.0.1, port - 9092
    </pre>

## Progress

### Finished

 *  server part of c api
 *  client part of python api

### Todo

 *  client part of c api
 *  server part of python api
 *  both client and server part of php api
 *  monitoring, such as current servers and clients online, connections on each server, number of callings received by each server etc.
 *  managing, such as kick off unfriendly clients, limit the calling rates of client etc.

[thrift]: http://thrift.apache.org/ "Thrift"
[zookeeper]: http://zookeeper.apache.org/ "ZooKeeper" 
[gflags]: https://code.google.com/p/gflags/ "gflags"
[json-c]: https://github.com/json-c/json-c "josn-c"
