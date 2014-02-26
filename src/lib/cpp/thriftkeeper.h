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

private:
	zhandle_t *zh;
	string servicePath;

public:
	ThriftKeeper(const string host, const string serviceName,
		ZooLogLevel debugLevel = ZOO_LOG_LEVEL_DEBUG);
	bool registerServiceNode(string nodeName = "", const string data = "");

private:
	static void watcherCallback(zhandle_t *zh, int type, int state,
		const char *path, void *watcherCtx);
};

}

#endif /* THRIFTKEEPER_H_ */
