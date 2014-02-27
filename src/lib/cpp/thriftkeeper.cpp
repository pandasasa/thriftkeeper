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

static ThriftKeeper *pTk;

void zkWatcherCallback(zhandle_t *zh, int type, int state, const char *path,
	void *watcherCtx) {
	cerr << "notification received, type - " << type << ", state - "
		<< state << ", path - " << path << endl;

	if (type == ZOO_SESSION_EVENT) {
		if (state == ZOO_EXPIRED_SESSION_STATE) {
			if (pTk->reRegisterServiceNode()) {
				cerr << "session expired and register succeed" << endl;
			} else {
				cerr << "session expired but register failed" << endl;
			}
		}
	}
}

ThriftKeeper::ThriftKeeper(const string zkHost, ZooLogLevel zkDebugLevel):
	_registered(false) {
	zoo_set_debug_level(zkDebugLevel);

	pTk = this;
	zh = zookeeper_init(zkHost.c_str(), zkWatcherCallback, 1000, 0, NULL, 0);
}

bool ThriftKeeper::registerServiceNode(const string serviceName, const string nodeName,
	const string nodeData) {
	this->serviceName = serviceName;
	if (nodeName == "") {
		char hostname[128];
		gethostname(hostname, sizeof(hostname));
		this->nodeName = hostname;
	} else {
		this->nodeName = nodeName;
	}
	this->nodeData = nodeData;

	if (_registerServiceNode()) {
		_registered = true;
		return true;
	} else {
		return false;
	}
}

bool ThriftKeeper::_registerServiceNode() {
	string path = getNodePath();
	int ret = zoo_create(zh, path.c_str(), nodeData.c_str(), nodeData.length(),
		&ZOO_OPEN_ACL_UNSAFE, ZOO_EPHEMERAL, NULL, 0);
	if (ret) {
		cerr << "create node failed, ret - " << ret << endl;
		return false;
	} else {
		return true;
	}
}

bool ThriftKeeper::reRegisterServiceNode() {
	if (!_registered) {
		return false;
	}

	return _registerServiceNode();
}

string ThriftKeeper::getNodePath() {
	return "/thriftkeeper/" + serviceName + "/providers/" + nodeName;
}

}
