/*
 * thriftkeeper.h
 *
 *  Created on: 2014年2月26日
 *      Author: jagger
 */

#ifndef THRIFTKEEPER_H_
#define THRIFTKEEPER_H

#include <stdbool.h>

#include <json-c/json.h>
#include <zookeeper/zookeeper.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
	TK_LOG_LEVEL_ERROR = 1,
	TK_LOG_LEVEL_WARN  = 2,
	TK_LOG_LEVEL_INFO  = 3,
	TK_LOG_LEVEL_DEBUG = 4
} tk_log_level_t;

#define TK_LOG_ERROR(...) if(tk_log_level >= TK_LOG_LEVEL_ERROR) \
    tk_log_message(TK_LOG_LEVEL_ERROR, __VA_ARGS__)
#define TK_LOG_WARN(...) if(tk_log_level >= TK_LOG_LEVEL_WARN) \
    tk_log_message(TK_LOG_LEVEL_WARN, __VA_ARGS__)
#define TK_LOG_INFO(...) if(tk_log_level >= TK_LOG_LEVEL_INFO) \
    tk_log_message(TK_LOG_LEVEL_INFO, __VA_ARGS__)
#define TK_LOG_DEBUG(...) if(tk_log_level == TK_LOG_LEVEL_DEBUG) \
    tk_log_message(TK_LOG_LEVEL_DEBUG, __VA_ARGS__)

void tk_init(const char *hosts, const char *service_name, const char *node_name,
	json_object *node_data, bool is_provider);

void tk_log_message(tk_log_level_t level, const char *format, ...);
void tk_set_log_level(tk_log_level_t level);
void tk_set_log_stream(FILE *stream);

#ifdef __cplusplus
}
#endif

#endif /* THRIFTKEEPER_H_ */
