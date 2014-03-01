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

ThriftKeeper *ptk;

void ZkWatcher(zhandle_t *zh, int type, int state, const char *path,
	void *watcherCtx) {
	cerr << "notification received, type - " << type << ", state - "
		<< state << ", path - " << path << endl;

	if (type == ZOO_SESSION_EVENT) {
		if (ptk->state_ == 0 && state == ZOO_CONNECTED_STATE) {
			if (ptk->register_node()) {
				cerr << "register succeed" << endl;
			} else {
				cerr << "register failed" << endl;
			}
			ptk->state_ = state;
		} else if (state == ZOO_EXPIRED_SESSION_STATE) {
			if (ptk->register_node()) {
				cerr << "session expired and register succeed" << endl;
			} else {
				cerr << "session expired but register failed" << endl;
			}
		}
	}
}

ThriftKeeper::ThriftKeeper(const string hosts, const string service_name,
	const string node_name, Json::Value node_data, bool is_provider,
	ZooLogLevel zk_debug_level): state_(0), node_data_(Json::objectValue),
	is_provider_(false) {
	service_name_ = service_name;
	if (node_name == "") {
		char hostname[128];
		gethostname(hostname, sizeof(hostname));
		node_name_ = hostname;
	} else {
		node_name_ = node_name;
	}
	node_data_ = node_data;
	is_provider_ = is_provider;

	zoo_set_debug_level(zk_debug_level);
	ptk = this;
	zh_ = zookeeper_init(hosts.c_str(), ZkWatcher, 1000, 0, NULL, 0);
}

bool ThriftKeeper::set_node_data_item(string key, Json::Value value) {
	node_data_[key] = value;
	return true;
}

bool ThriftKeeper::register_node() {
	string path = get_node_path();

	Json::FastWriter writer;
	string data = writer.write(node_data_);
	int ret = zoo_create(zh_, path.c_str(), data.c_str(), data.length(),
		&ZOO_OPEN_ACL_UNSAFE, ZOO_EPHEMERAL, NULL, 0);
	if (ret) {
		cerr << "create node failed, ret - " << ret << endl;
		return false;
	} else {
		return true;
	}
}

string ThriftKeeper::get_service_path() {
	return "/thriftkeeper/" + service_name_;
}

string ThriftKeeper::get_node_path() {
	if (is_provider_) {
		return get_service_path() + "/providers/" + node_name_;
	} else {
		return get_service_path() + "/consumers/" + node_name_;
	}
}

}
