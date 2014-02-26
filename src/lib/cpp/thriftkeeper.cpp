/*
 * thriftkeeper.cpp
 *
 *  Created on: 2014年2月26日
 *      Author: jagger
 */

#include <iostream>
#include <cstdlib>
#include <sys/unistd.h>

#include "thriftkeeper.h"

using namespace std;

namespace thriftkeeper {

ThriftKeeper::ThriftKeeper(const string host, const string serviceName,
	ZooLogLevel debugLevel) {
	zoo_set_debug_level(debugLevel);

	zh = zookeeper_init(host.c_str(), ThriftKeeper::watcherCallback, 1000,
		0, NULL, 0);

	servicePath = "/thriftkeeper/" + serviceName;
}

bool ThriftKeeper::registerServiceNode(string nodeName, const string data) {
	if (nodeName == "") {
		char hostname[128];
		gethostname(hostname, sizeof(hostname));
		nodeName = hostname;
	}
	string path = servicePath + "/providers/" + nodeName;
	int ret = zoo_create(zh, path.c_str(), data.c_str(), data.length(),
		&ZOO_OPEN_ACL_UNSAFE, ZOO_EPHEMERAL, NULL, 0);
	if (ret) {
		cerr << "create node failed, ret - " << ret << endl;
		return false;
	}
	return true;
}

void ThriftKeeper::watcherCallback(zhandle_t *zh, int type, int state,
	const char *path, void *watcherCtx) {
	cout << "notification received, type - " << type << ", state - "
		<< state << ", path - " << path << endl;
}

}
