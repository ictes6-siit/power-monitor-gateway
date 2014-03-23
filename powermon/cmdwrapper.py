__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'

import sys, threading, logging
from operator import xor
from .cmdformat import *

class CmdStatus(object):
    START_MSG = 'START_MSG'
    IN_MSG = 'IN_MSG'
    MSG_OK = 'MSG_OK'
    ERROR = 'ERROR'

class CmdWrapper(object):
    # internal state
    (WAIT_SYNC, WAIT_CMD, WAIT_LEN, WAIT_DATA, WAIT_FCS) = range(5)

    log = logging.getLogger('powermon.cmdwrapper.CmdWrapper')

    def __init__(self,
            sync=b'\xAA'):
        self.sync = sync
        self.state = self.WAIT_SYNC
        self.last_message = bytearray()
        self.message_buf = bytearray()
        self.last_cmd = ''
        self.last_error = ''
        self.len = 0

    def wrap(self, cmdFormat, cmdContainer):
        cmdName = cmdFormat.name
        data = cmdFormat.build(cmdContainer)
        kwargs = {
            'sync' : SYNC_BYTE,
            'cmdType' : cmdName,
            'len' : len(data),
            'fcs' : 0
        }
        # copy element from container to kwargs
        for elem in cmdContainer:
            if not elem.startswith("_"):
                kwargs[elem] = cmdContainer[elem]

        wrapped = Cmd_Format.build(Container(**kwargs))
        wrapped = bytearray(wrapped)

        # add FCS to last byte.
        fcs = 0
        for byte in wrapped[1:-1]:
            fcs = xor(fcs, byte)
        wrapped[-1] = fcs
        return wrapped


    def input(self, new_byte):
        if self.state == self.WAIT_SYNC:
            if new_byte == self.sync:
                self.message_buf += new_byte
                self.state = self.WAIT_CMD
                return CmdStatus.START_MSG
            else:
                self.last_error = 'Expected header (0x%02X), got 0x%02X' % (
                    ord(self.sync), ord(new_byte))
                return CmdStatus.ERROR
        elif self.state == self.WAIT_CMD:
            # Todo: un-support command
            self.message_buf += new_byte
            self.state = self.WAIT_LEN
            return CmdStatus.IN_MSG
        elif self.state == self.WAIT_LEN:
            self.message_buf += new_byte
            self.len = ord(new_byte)
            if(self.len == 0):
                self.state = self.WAIT_FCS
            else:
                self.state = self.WAIT_DATA
            return CmdStatus.IN_MSG
        elif self.state == self.WAIT_DATA:
            self.message_buf += new_byte
            self.len -= 1
            if self.len == 0:
                self.state = self.WAIT_FCS
            return CmdStatus.IN_MSG
        elif self.state == self.WAIT_FCS:
            self.message_buf += new_byte
            check_fcs = 0
            for byte in self.message_buf[1:]:
                check_fcs = xor(check_fcs, byte)

            if check_fcs == 0:
                return self._finish_msg()
            else:
                self.last_error = 'Invalid Checksum'
                self.message_buf = ''
                self.state = self.WAIT_SYNC
                return CmdStatus.ERROR

    def _finish_msg(self):
        self.state = self.WAIT_SYNC
        self.last_message = self.message_buf
        self.last_cmd = Cmd_Format.parse(self.last_message)
        self.message_buf = bytearray()
        return CmdStatus.MSG_OK
