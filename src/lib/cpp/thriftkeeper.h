/*
 * thriftkeeper.h
 *
 *  Created on: 2014年2月26日
 *      Author: jagger
 */

#ifndef THRIFTKEEPER_H_
#define THRIFTKEEPER_H_

#include <string>

#include <zookeeper/zookeeper.h>
#include <json/json.h>

using namespace std;

namespace thriftkeeper {

class ThriftKeeper {

public:
	int state_;

	ThriftKeeper(const string hosts = "127.0.0.1:2181", const string service_name = "tutorial",
		const string node_name = "", Json::Value node_data = Json::objectValue,
		bool is_provider = true, ZooLogLevel zk_debug_level = ZOO_LOG_LEVEL_DEBUG);
	bool set_node_data_item(string key, Json::Value value);
	bool register_node();

private:
	zhandle_t *zh_;
	string service_name_;
	string node_name_;
	Json::Value node_data_;
	bool is_provider_;

	string get_service_path();
	string get_node_path();
};

}

#endif /* THRIFTKEEPER_H_ */
