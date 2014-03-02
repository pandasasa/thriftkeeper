#!/usr/bin/env python

import sys
import time
import argparse
import logging

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thriftkeeper import ThriftKeeper
from thrift.transport.TTransport import TTransportException

from tutorial import Calculator
from tutorial.ttypes import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def rpc(tk, procedure, params, logger):
    host, port = tk.get_provider_address().split(':')
    port = int(port)
    logger.info("provider address, host - {}, port - {}".format(host, port))

    socket = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Calculator.Client(protocol)
    transport.open()
    
    if procedure == 'ping':
        client.ping()
    else:
        logger.error('unrecognized procedure {}'.format(procedure))
        sys.exit(1)
    
    transport.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculator client with zookeeper.')
    parser.add_argument('--hosts', dest='hosts', action='store', 
        default='127.0.0.1:2181,127.0.0.1:2182,127.0.0.1:2183',
        help='the hosts of zookeeper')
    parser.add_argument('--service_name', dest='service_name', action='store', default='tutorial',
        help='the name of rpc service to request')
    parser.add_argument('--count', dest='count', action='store', default=0, type=int,
        help='how many times to request, default to loop forever')
    parser.add_argument('--interval', dest='interval', action='store', default=1, type=int,
        help='wait for how many seconds between two requests')
    parser.add_argument('--log_level', dest='log_level', action='store', 
        choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO',
        help='log level')
    parser.add_argument('procedure', metavar='PROCEDURE', nargs=1,
        help='remote procedure to call')
    parser.add_argument('params', metavar='PARAM', nargs='*',
        help='parameters of remote procedure')
    
    args = parser.parse_args()
    
    if args.log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif args.log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif args.log_level == 'WARN':
        logger.setLevel(logging.WARN)
    elif args.log_level == 'ERROR':
        logger.setLevel(logging.ERROR)
    
    tk = ThriftKeeper(args.hosts, args.service_name, is_provider=False, logger=logger)
    
    c = 0
    while True:
        try:
            rpc(tk, args.procedure[0], args.params, logger)
        except TTransportException as e:
            logger.error("remote procedure call failed, exception - {}".format(e))
        
        c += 1
        if args.count > 0 and c == args.count:
            break;
        
        logger.info('called procedure {} {} times'.format(args.procedure[0], c))
        
        time.sleep(args.interval)
