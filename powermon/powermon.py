__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'

import sys, re, logging, weakref, time, threading, abc, codecs
from datetime import datetime
from .cmdwrapper import *
from .serialcomm import SerialComm
from pydispatch import dispatcher

class PowerMon(SerialComm):
    log = logging.getLogger('powermon.powermon.PowerMon')

    def __init__(self, port, baudrate=115200):
        self.baudrate = baudrate
        self.port = port
        super(PowerMon, self).__init__(port, baudrate, event_cmd_callback_func=self._cmd_handler)

    def _cmd_handler(self, cmd):
        threading.Thread(target=self.__threaded_cmd_handler, kwargs={'cmds': cmd}).start()

    def __threaded_cmd_handler(self, cmds):
        for cmd in cmds:
            dispatcher.send(sender=self, signal=cmd.cmdType, cmd=cmd)
        return

    def add_handler(self, cmd_format, callback_func):
        pass

    def send_cmd(self, cmd_format, cmd_container, wait_for_response=True, timeout=5, expected_resp_cmd=None):
        return self.write(cmd_format, cmd_container, wait_for_response, timeout, expected_resp_cmd)