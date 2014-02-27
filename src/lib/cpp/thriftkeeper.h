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

using namespace std;

namespace thriftkeeper {

class ThriftKeeper {

public:
	ThriftKeeper(const string zkHost, ZooLogLevel zkDebugLevel = ZOO_LOG_LEVEL_DEBUG);
	bool registerServiceNode(const string serviceName, const string nodeName = "",
		const string nodeData = "");
	bool reRegisterServiceNode();
	string getNodePath();

private:
	zhandle_t *zh;
	string serviceName;
	string nodeName;
	string nodeData;
	bool _registered;

	bool _registerServiceNode();
};

}

#endif /* THRIFTKEEPER_H_ */
