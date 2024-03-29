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

static tk_log_level_t tk_log_level = TK_LOG_LEVEL_INFO;
static FILE *tk_log_stream = stderr;

static char tk_hosts[128];
static char tk_service_name[128];
static char tk_node_name[128];
static json_object *tk_node_data = NULL;
static bool tk_is_provider = true;
static zhandle_t *tk_zh = NULL;
static bool tk_registered = false;

static void tk_global_watcher(zhandle_t *zh, int type, int state, const char *path,
	void *watcherCtx);

static void tk_init_handle();
static bool tk_register_node();
static void get_service_path(char *path);
static void get_node_path(char *path);

void tk_log_message(tk_log_level_t level, const char *format, ...)
{
	if (level <= tk_log_level) {
	    va_list va;
	    va_start(va, format);
		vfprintf(tk_log_stream, format, va);
	    va_end(va);
	}
}

void tk_set_log_level(tk_log_level_t level)
{
	tk_log_level = level;

	zoo_set_debug_level((ZooLogLevel) tk_log_level);
}

void tk_set_log_stream(FILE *stream)
{
	tk_log_stream = stream;
}

void tk_global_watcher(zhandle_t *zh, int type, int state, const char *path,
	void *context)
{
	TK_LOG_INFO("notification received, type - %d, state - %d, path - %s\n", type, state, path);

	if (type == ZOO_SESSION_EVENT) {
		if (!tk_registered && state == ZOO_CONNECTED_STATE) {
			if (tk_register_node()) {
				TK_LOG_INFO("register succeed\n");
			} else {
				TK_LOG_ERROR("register failed\n");
			}
			tk_registered = true;
		} else if (state == ZOO_EXPIRED_SESSION_STATE) {
			tk_init_handle();
			tk_registered = false;
			TK_LOG_WARN("session expired, reinited\n");
		}
	}
}

void tk_init(const char *hosts, const char *service_name, const char *node_name,
	json_object *node_data, bool is_provider)
{
	strncpy(tk_hosts, hosts, sizeof(tk_hosts) - 1);
	strncpy(tk_service_name, service_name, sizeof(tk_service_name) - 1);
	if (strlen(node_name) == 0) {
		gethostname(tk_node_name, sizeof(tk_node_name) - 1);
	} else {
		strncpy(tk_node_name, node_name, sizeof(tk_node_name) - 1);
	}
	tk_node_data = node_data;
	tk_is_provider = is_provider;

	zoo_set_debug_level((ZooLogLevel) tk_log_level);

	tk_init_handle();
}

void tk_init_handle()
{
	if (tk_zh != NULL) {
		zookeeper_close(tk_zh);
	}

	tk_zh = zookeeper_init(tk_hosts, tk_global_watcher, 1000, 0, NULL, 0);
}

bool tk_register_node()
{
	char path[128];
	get_node_path(path);

	const char *data = json_object_to_json_string(tk_node_data);
	int ret = zoo_create(tk_zh, path, data, strlen(data), &ZOO_OPEN_ACL_UNSAFE,
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
	sprintf(path, "/thriftkeeper/%s",  tk_service_name);
}

void get_node_path(char *path)
{
	char service_path[128];
	get_service_path(service_path);

	if (tk_is_provider) {
		sprintf(path, "%s/providers/%s", service_path, tk_node_name);
	} else {
		sprintf(path, "%s/consumers/%s", service_path, tk_node_name);
	}
}

