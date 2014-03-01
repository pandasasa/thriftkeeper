/*
 * thriftkeeper.cpp
 *
 *  Created on: 2014年2月26日
 *      Author: jagger
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <sys/unistd.h>
#include <json-c/json.h>

#include <zookeeper/zookeeper.h>

#include "thriftkeeper.h"

#define FORMAT_TK_LOG_BUF_SIZE 4096

static zk_log_level_t zk_log_level = TK_LOG_LEVEL_INFO;
static FILE *zk_log_stream = stderr;

static char zk_hosts[128];
static char zk_service_name[128];
static char zk_node_name[128];
static const json_object *zk_node_data = NULL;
static bool zk_is_provider = true;
static zhandle_t *zh = NULL;
static bool registered = false;

static void zk_global_watcher(zhandle_t *zh, int type, int state, const char *path,
	void *watcherCtx);

static void tk_init_handle();
static bool tk_register_node();
static void get_service_path(char *path);
static void get_node_path(char *path);

void tk_log_message(zk_log_level_t level, const char *format, ...)
{
	if (level <= zk_log_level) {
	    va_list va;
	    va_start(va, format);
		vfprintf(zk_log_stream, format, va);
	    va_end(va);
	}
}

void tk_set_log_level(zk_log_level_t level)
{
	zk_log_level = level;

	zoo_set_debug_level((ZooLogLevel) zk_log_level);
}

void tk_set_log_stream(FILE *stream)
{
	zk_log_stream = stream;
}

void zk_global_watcher(zhandle_t *zh, int type, int state, const char *path,
	void *watcherCtx)
{
	TK_LOG_INFO("notification received, type - %d, state - %d, path - %s\n", type, state, path);

	if (type == ZOO_SESSION_EVENT) {
		if (!registered && state == ZOO_CONNECTED_STATE) {
			if (tk_register_node()) {
				TK_LOG_INFO("register succeed\n");
			} else {
				TK_LOG_ERROR("register failed\n");
			}
			registered = true;
		} else if (state == ZOO_EXPIRED_SESSION_STATE) {
			tk_init_handle();
			registered = false;
			TK_LOG_WARN("session expired, reinited\n");
		}
	}
}

void tk_init(const char *hosts, const char *service_name, const char *node_name,
	const json_object *node_data, bool is_provider)
{
	strncpy(zk_hosts, hosts, sizeof(zk_hosts));
	strncpy(zk_service_name, service_name, sizeof(zk_service_name));
	if (strlen(node_name) == 0) {
		gethostname(zk_node_name, sizeof(zk_node_name));
	} else {
		strncpy(zk_node_name, node_name, sizeof(zk_node_name));
	}
	zk_node_data = node_data;
	zk_is_provider = is_provider;

	zoo_set_debug_level((ZooLogLevel) zk_log_level);

	tk_init_handle();
}

void tk_init_handle()
{
	if (zh != NULL) {
		zookeeper_close(zh);
	}

	zh = zookeeper_init(zk_hosts, zk_global_watcher, 1000, 0, NULL, 0);
}

bool tk_register_node()
{
	char path[128];
	get_node_path(path);

	char data[128];
	int ret = zoo_create(zh, path, data, sizeof(data), &ZOO_OPEN_ACL_UNSAFE,
		ZOO_EPHEMERAL, NULL, 0);
	if (ret) {
		TK_LOG_ERROR("create node failed, ret - %d\n", ret);
		return false;
	} else {
		return true;
	}
}

void get_service_path(char *path)
{
	sprintf(path, "/thriftkeeper/%s",  zk_service_name);
}

void get_node_path(char *path)
{
	char service_path[128];
	get_service_path(service_path);

	if (zk_is_provider) {
		sprintf(path, "%s/providers/%s", service_path, zk_node_name);
	} else {
		sprintf(path, "%s/consumers/%s", service_path, zk_node_name);
	}
}

