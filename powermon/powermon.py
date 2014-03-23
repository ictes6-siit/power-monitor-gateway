__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'

import sys, re, logging, weakref, time, threading, abc, codecs
from datetime import datetime
from .cmdwrapper import *
from .serialcomm import SerialComm

class PowerMon(SerialComm):
    log = logging.getLogger('powermon.powermon.PowerMon')

    def __init__(self, port, baudrate=115200):
        super(PowerMon, self).__init__(port, baudrate, event_cmd_callback_func=self._cmd_handler)

    def _cmd_handler(self, cmd):
        print('handler : ' , cmd)

