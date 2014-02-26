#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,tornado,utf8strings
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None

from tornado import gen
from tornado import stack_context

class Iface(object):
  def getStruct(self, key, callback):
    """
    Parameters:
     - key
    """
    pass


class Client(Iface):
  def __init__(self, transport, iprot_factory, oprot_factory=None):
    self._transport = transport
    self._iprot_factory = iprot_factory
    self._oprot_factory = (oprot_factory if oprot_factory is not None
                           else iprot_factory)
    self._seqid = 0
    self._reqs = {}

  @gen.engine
  def recv_dispatch(self):
    """read a response from the wire. schedule exactly one per send that
    expects a response, but it doesn't matter which callee gets which
    response; they're dispatched here properly"""

    # wait for a frame header
    frame = yield gen.Task(self._transport.readFrame)
    tr = TTransport.TMemoryBuffer(frame)
    iprot = self._iprot_factory.getProtocol(tr)
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    method = getattr(self, 'recv_' + fname)
    method(iprot, mtype, rseqid)

  def getStruct(self, key, callback):
    """
    Parameters:
     - key
    """
    self._seqid += 1
    self._reqs[self._seqid] = callback
    self.send_getStruct(key)
    self.recv_dispatch()

  def send_getStruct(self, key):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('getStruct', TMessageType.CALL, self._seqid)
    args = getStruct_args()
    args.key = key
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_getStruct(self, iprot, mtype, rseqid):
    callback = self._reqs.pop(rseqid)
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      callback(x)
      return
    result = getStruct_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      callback(result.success)
      return
    callback(TApplicationException(TApplicationException.MISSING_RESULT, "getStruct failed: unknown result"))
    return


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["getStruct"] = Processor.process_getStruct

  @gen.engine
  def process(self, transport, iprot_factory, oprot, callback):
    # wait for a frame header
    frame = yield gen.Task(transport.readFrame)
    tr = TTransport.TMemoryBuffer(frame)
    iprot = iprot_factory.getProtocol(tr)

    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
    else:
      yield gen.Task(self._processMap[name], self, seqid, iprot, oprot)
    callback()

  @gen.engine
  def process_getStruct(self, seqid, iprot, oprot, callback):
    args = getStruct_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = getStruct_result()
    result.success = yield gen.Task(self._handler.getStruct, args.key)
    oprot.writeMessageBegin("getStruct", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()
    callback()


# HELPER FUNCTIONS AND STRUCTURES

class getStruct_args(object):
  """
  Attributes:
   - key
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'key', None, None, ), # 1
  )

  def __init__(self, key=None,):
    self.key = key

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.key = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('getStruct_args')
    if self.key is not None:
      oprot.writeFieldBegin('key', TType.I32, 1)
      oprot.writeI32(self.key)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getStruct_result(object):
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (SharedStruct, SharedStruct.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = SharedStruct()
          self.success.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('getStruct_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
