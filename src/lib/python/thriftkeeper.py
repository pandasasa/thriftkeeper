import logging
import random
import bisect
import itertools
import json
import socket

import zookeeper

LOAD_BANLANCE_STRATEGY_RANDOM = 1
LOAD_BANLANCE_STRATEGY_WEIGHT = 2

ZOO_OPEN_ACL_UNSAFE = {"perms":0x1f, "scheme":"world", "id" :"anyone"}
    
class ThriftKeeper:
    
    def __init__(self, hosts='127.0.0.1:2181', service_name='tutorial', 
        node_name=None, node_data=None, is_provider=False, logger=None):
        self._hosts = hosts
        self._service_name = service_name
        if node_name is None:
            self._node_name = socket.gethostname()
        else:
            self._node_name = node_name
        self._node_data = node_data if node_data is dict else {}
        self._is_provider = is_provider
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger
            
        if self._logger.level == logging.DEBUG:
            zk_debug_level = zookeeper.LOG_LEVEL_DEBUG
        elif self._logger.level == logging.WARN:
            zk_debug_level = zookeeper.LOG_LEVEL_WARN
        elif self._logger.level == logging.INFO:
            zk_debug_level = zookeeper.LOG_LEVEL_INFO
        else:
            zk_debug_level = zookeeper.LOG_LEVEL_ERROR
        
        zookeeper.set_debug_level(zk_debug_level)
        
        self._init_handle()
    
    def get_provider_address(self, strategy=LOAD_BANLANCE_STRATEGY_RANDOM):
        return self._get_provider(strategy)['data']['address']
        
    def _init_handle(self):
        if hasattr(self, '_zh'):
            zookeeper.close(self._zh)
        
        self._zh = zookeeper.init(self._hosts, self._global_watcher(), 1000)
    
    def _global_watcher(self):
        def watcher(zh, type, state, path):
            self._logger.info('notification received, type - {}, state - {}, path - {}'
                .format(type, state, path))
            
            if type == zookeeper.SESSION_EVENT:
                if ((not hasattr(self, 'registered') or not self.registered) 
                    and state == zookeeper.CONNECTED_STATE):
                    if self._register_node():
                        self._logger.info("register succeed")
                    else:
                        self._logger.error("register failed")
                    self.registered = True
                elif state == zookeeper.EXPIRED_SESSION_STATE:
                    self._init_handle()
                    self.registered = False
                    self._logger.warn("session expired, reinited");
        
        return watcher
    
    def _register_node(self):
        path = self._get_node_path()
        data = json.dumps(self._node_data)
        try:
            created_path = zookeeper.create(self._zh, path, data, [ZOO_OPEN_ACL_UNSAFE],
                zookeeper.EPHEMERAL)
        except zookeeper.ZooKeeperException as e:
            self._logger.error("create node failed, exception - {}".format(e))
            return False
        return True
        
    def _get_provider(self, strategy=LOAD_BANLANCE_STRATEGY_RANDOM):
        providers = self._get_providers()
        
        if len(providers) == 0:
            self._logger.error('no provider found')
            return None
        
        if strategy == LOAD_BANLANCE_STRATEGY_RANDOM:
            provider = random.choice(providers)
        elif strategy == LOAD_BANLANCE_STRATEGY_WEIGHT:
            provider = ThriftKeeper._choose_provider_by_weight(providers)
        
        return provider
    
    def _get_service_path(self):
        return '/thriftkeeper/{}'.format(self._service_name)
        
    def _get_node_path(self):
        if self._is_provider:
            return '{}/privoders/{}'.format(self._get_service_path(), 
                self._node_name)
        else:
            return '{}/consumers/{}'.format(self._get_service_path(), 
                self._node_name)
    
    def _get_providers(self):
        if not hasattr(self, '_providers'):
            providers_path = '{}/providers'.format(self._get_service_path())
            try:
                children = zookeeper.get_children(self._zh, providers_path, 
                    self._get_providers_watcher())
            except zookeeper.ZooKeeperException as e:
                self._logger.error("create node failed, exception - {}".format(e))
                return []
            
            self._providers = []
            for name in children:
                data, stat = self._get_provider_data(name)
                self._providers.append({'name': name, 'data': data, 'stat': stat})
        
        return self._providers
    
    def _get_provider_data(self, name):
        provider_path = '{}/providers/{}'.format(self._get_service_path(), name)
        try:
            data, stat = zookeeper.get(self._zh, provider_path, self._get_provider_watcher(name))
        except zookeeper.ZooKeeperException as e:
            self._logger.error("get data failed, exception - {}".format(e))
            return {}, {}
        
        return json.loads(data), stat
        
    def _get_providers_watcher(self):
        def watcher(zh, type, state, path):
            self._logger.info('providers changed, type - {}, state - {}, path - {}'
                .format(type, state, path))
            
            if type == zookeeper.DELETED_EVENT:
                self._providers = []
        
        return watcher
    
    def _get_provider_watcher(self, name):
        def watcher(zh, type, state, path):
            self._logger.info('provider {} changed, type - {}, state - {}, path - {}'
                .format(name, type, state, path))
            
            if type == zookeeper.CHANGED_EVENT:
                self._get_provider_data(name)
            if type == zookeeper.DELETED_EVENT:
                self._providers = [provider for provider in self._providers 
                    if provider['name'] != name]
        
        return watcher
    
    @staticmethod
    def _choose_provider_by_weight(providers):
        weights = [provider['data']['weight'] for provider in providers]
        partsums = list(itertools.accumulate(weights))
        return self._providers[bisect.bisect_right(partsums, random.random() * partsums[-1])]
