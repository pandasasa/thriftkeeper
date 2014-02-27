import logging

from kazoo.client import KazooClient
from kazoo.exceptions import ZookeeperError
from kazoo.protocol.states import EventType
    
class ThriftKeeper:
    LOAD_BANLANCE_STRATEGY_RANDOM = 1
    LOAD_BANLANCE_STRATEGY_WEIGHT = 2
    
    def __init__(self, hosts='127.0.0.1:2181', service_name='tutorial', 
        node_name=None, is_provider=False, logger=None):
        self.service_name=service_name
        self.node_name=node_name
        self.is_provider=is_provider
        if logger is None:
            self.logger=logging.getLogger(__name__)
        else:
            self.logger=logger
        
        self.zk=KazooClient(hosts)
        self.zk.add_listener(self.get_connection_listener())
        self.zk.start(1)
        
        self.register_node()
        
        self.get_providers()
    
    def register_node(self):
        path=self.get_node_path()
        self.zk.create(path, ephemeral=True)
    
    def get_connection_listener(self):
        def listener(state):
            self.logger.info('connection state changed, state - {}'.format(state))
        
        return listener
    
    def get_providers_watcher(self):
        def watcher(event):
            if event.type in (EventType.CHILD):
                self.get_providers()
        
        return watcher
    
    def get_service_path(self):
        return '/thriftkeeper/{}'.format(self.service_name)
        
    def get_node_path(self):
        if self.is_provider:
            return '/privoders/{}'.format(self.get_service_path(), 
                self.service_name, self.node_name)
        else:
            return '/consumers/{}'.format(self.get_service_path(), 
                self.service_name, self.node_name)
    
    def get_providers(self):
        self._providers = self.zk.get_children('{}/providers'.format(
            self.get_service_path()), self.get_providers_watcher())
        
    def get_provider(self, strategy=ThriftKeeper.LOAD_BANLANCE_STRATEGY_RANDOM):
        pass
