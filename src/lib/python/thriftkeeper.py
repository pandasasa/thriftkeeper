import logging
import random
import bisect
import itertools
import json
import socket

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState, EventType
from kazoo.exceptions import KazooException

LOAD_BANLANCE_STRATEGY_RANDOM = 1
LOAD_BANLANCE_STRATEGY_WEIGHT = 2
    
class ThriftKeeper:
    
    def __init__(self, hosts='127.0.0.1:2181', service_name='tutorial', 
        node_name=None, node_data=None, is_provider=False, logger=None):
        self.service_name = service_name
        if node_name is None:
            self.node_name = socket.gethostname()
        else:
            self.node_name = node_name
        self.node_data = node_data if node_data is dict else {}
        self.is_provider = is_provider
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        
        self._zk = KazooClient(hosts, logger=self.logger)
        self._zk.add_listener(self._get_connection_listener())
        self._zk.start()
        
    def get_provider_address(self, strategy=LOAD_BANLANCE_STRATEGY_RANDOM):
        return self._get_provider(strategy)['data']['address']
        
    def _get_provider(self, strategy=LOAD_BANLANCE_STRATEGY_RANDOM):
        if not hasattr(self, '_providers'):
            self._get_providers()
        
        if len(self._providers) == 0:
            self.logger.error('no provider found')
            return None
        
        if strategy == LOAD_BANLANCE_STRATEGY_RANDOM:
            provider = random.choice(self._providers)
        elif strategy == LOAD_BANLANCE_STRATEGY_WEIGHT:
            provider = self._choose_provider_by_weight()
        
        return provider
    
    def _get_connection_listener(self):
        def listener(state):
            self.logger.info('connection state changed, state - {}'.format(state))
            
            if ((not hasattr(self, '_state') or self._state == KazooState.LOST) 
                and state == KazooState.CONNECTED):
                self._state = state
                self._register_node()
        
        return listener
    
    def _register_node(self):
        path = self._get_node_path()
        data = json.dumps(self.node_data).encode('utf-8')
        self._zk.create(path, data, ephemeral=True)
    
    def _get_service_path(self):
        return '/thriftkeeper/{}'.format(self.service_name)
        
    def _get_node_path(self):
        if self.is_provider:
            return '{}/privoders/{}'.format(self._get_service_path(), 
                self.node_name)
        else:
            return '{}/consumers/{}'.format(self._get_service_path(), 
                self.node_name)
    
    def _get_providers(self):
        providers_path = '{}/providers'.format(self._get_service_path())
        children = self._zk.get_children(providers_path, 
            self._get_providers_watcher())
        
        self._providers = []
        for name in children:
            data, stat = self._get_provider_data(name)
            self._providers.append({'name': name, 'data': data, 'stat': stat})
    
    def _get_provider_data(self, name):
        provider_path = '{}/providers/{}'.format(self._get_service_path(), name)
        data, stat = self._zk.get(provider_path, self._get_provider_watcher(name))
        return json.loads(data.decode('utf-8')), stat
        
    def _get_providers_watcher(self):
        def watcher(event):
            self.logger.info('providers changed, event - {}'.format(event))
            
            if event.type == EventType.CHILD:
                self._get_providers()
            elif event.type == EventType.DELETED:
                self._providers = []
        
        return watcher
    
    def _get_provider_watcher(self, name):
        def watcher(event):
            self.logger.info('provider {} changed, event - {}'.format(name, 
                event))
            
            if event.type == EventType.CHANGED:
                self._get_provider_data(name)
            elif event.type == EventType.DELETED:
                self._providers = [provider for provider in self._providers 
                    if provider['name'] != name]
        
        return watcher
    
    def _choose_provider_by_weight(self):
        weights = [provider['data']['weight'] for provider in self._providers]
        partsums = list(itertools.accumulate(weights))
        return self._providers[bisect.bisect_right(partsums, random.random() * partsums[-1])]
