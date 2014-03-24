__author__ = 'Ratchasak Ranron'

import sys, threading, logging
import serial
from .cmdwrapper import *
from .exception import TimeoutException

class SerialComm(object):

    log = logging.getLogger('powermon.serialcomm.SerialComm')

    # Default timeout for serial port reads (in seconds)
    timeout = 1

    def __init__(self, port, baudrate=115200, event_cmd_callback_func=None, fatal_error_callback_func=None, *args, **kwargs):
        """ Constructor

        :param fatal_error_callback_func: function to call if a fatal error occurs in the serial device reading thread
        :type fatal_error_callback_func: func
        """
        self.serial = None
        self.rx_thread = None
        self.alive = False
        self.port = port
        self.baudrate = baudrate

        self._response_event = None # threading.Event()
        self._expect_resp_cmd = None # expected response terminator sequence
        self._response_cmd = None # Buffer containing response to a written command
        self._event_cmd = [] # Buffer containing cmd from an unsolicited notification from the modem
        # Reentrant lock for managing concurrent write access to the underlying serial port
        self._txLock = threading.RLock()
        self.cmd_wrapper = CmdWrapper()

        self.event_cmd_callback = event_cmd_callback_func or self._placeholder_callback
        self.fatal_error_callback = fatal_error_callback_func or self._placeholder_callback

    def connect(self):
        """ Connects to the device and starts the read thread """
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        # Start read thread
        self.alive = True
        self.rx_thread = threading.Thread(target=self._read_loop)
        self.rx_thread.daemon = True
        self.rx_thread.start()

    def close(self):
        """ Stops the read thread, waits for it to exit cleanly, then closes the underlying serial port """
        self.alive = False
        self.rx_thread.join()
        self.serial.close()

    def _handle_cmd_read(self, cmd, check_for_resp_cmd=True):
        #print 'sc.hlineread:',line
        if self._response_event and not self._response_event.is_set():
            # A response event has been set up (another thread is waiting for this response)
            self._response_cmd.append(cmd)
            if not check_for_resp_cmd or cmd.cmdType == self._expect_resp_cmd:
                # End of response reached; notify waiting thread
                #print 'response:', self._response
                self.log.debug('response: %s', self._response_cmd)
                self._response_event.set()
        else:
            # Nothing was waiting for this - treat it as a notification
            self._event_cmd.append(cmd)
            if self.serial.inWaiting() == 0:
                # print('notification:', self._event_cmd)
                self.log.debug('notification: %s', self._event_cmd)
                self.event_cmd_callback(self._event_cmd)
                self._event_cmd = []

    @staticmethod
    def _placeholder_callback(self, *args, **kwargs):
        """ Placeholder callback function (does nothing) """

    def _read_loop(self):
        """ Read thread main loop

        Reads cmd from the sensor device
        """
        try:
            while self.alive:
                data = self.serial.read(1)
                if len(data) != 0:
                    status = self.cmd_wrapper.input(data)
                    if status == CmdStatus.MSG_OK:
                        self._handle_cmd_read(self.cmd_wrapper.last_cmd)
        except serial.SerialException as e:
            self.alive = False
            try:
                self.serial.close()
            except Exception: #pragma: no cover
                pass
            # Notify the fatal error handler
            self.fatal_error_callback(e)

    def write(self, cmd_format, cmd_container, wait_for_response=True, timeout=5, expected_resp_cmd=None):
        with self._txLock:
            data = self.cmd_wrapper.wrap(cmd_format, cmd_container)
            if wait_for_response:
                if expected_resp_cmd:
                    self._expect_resp_cmd = expected_resp_cmd.name
                self._response_cmd = []
                self._response_event = threading.Event()
                self.serial.write(data)
                if self._response_event.wait(timeout):
                    self._response_event = None
                    self._expect_resp_cmd = False
                    return self._response_cmd[0]
                else: # Response timed out
                    self._response_event = None
                    self._expect_resp_cmd = False
                    if len(self._response_cmd) > 0:
                        # Add the partial response to the timeout exception
                        raise TimeoutException(self._response_cmd)
                    else:
                        raise TimeoutException()
            else:
                self.serial.write(data)
