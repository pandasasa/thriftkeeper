#!/usr/bin/env python

import sys
import time
import argparse
import logging
import pdb

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thriftkeeper import ThriftKeeper

from tutorial import Calculator
from tutorial.ttypes import *

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def rpc(tk, procedure, params, logger):
    host, port = tk.get_provider_address().split(':')

    socket = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Calculator.Client(protocol)
    transport.open()
    
    if procedure == 'ping':
        client.ping()
    else:
        print('unrecognized procedure {}'.format(procedure))
        sys.exit(1)
    
    transport.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculator client with zookeeper.')
    parser.add_argument('--zk_hosts', dest='zk_hosts', action='store', default='127.0.0.1:2181',
                       help='the hosts of zookeeper service')
    parser.add_argument('--zk_service', dest='zk_service', action='store', default='tutorial',
                       help='the nam of rpc service to request')
    parser.add_argument('--count', dest='count', action='store', default=0, type=int,
                       help='how many times to request, default to loop forever')
    parser.add_argument('--interval', dest='interval', action='store', default=1, type=int,
                       help='wait for how many seconds between two requests')
    parser.add_argument('procedure', metavar='PROCEDURE', nargs=1,
                       help='remote procedure to call')
    parser.add_argument('params', metavar='PARAM', nargs='*',
                       help='parameters of remote procedure')
    
    args = parser.parse_args()
    
    tk = ThriftKeeper(args.zk_hosts, args.zk_service, is_provider=False, 
        logger = logger)
    
    c = 0
    while True:
        rpc(tk, args.procedure[0], args.params, logger)
        
        c += 1
        if count > 0 and c == count:
            break;
        
        logger.info('called procedure {} {} times'.format(args.procedure[0], c))
        
        time.sleep(interval)
