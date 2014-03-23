__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'


class PowerMonException(Exception):
    """ Base exception raised for error conditions when interacting with the GSM modem """

class TimeoutException(PowerMonException):
    """ Raised when a write command times out """

    def __init__(self, data=None):
        """ @param data: Any data that was read was read before timeout occurred (if applicable) """
        super(TimeoutException, self).__init__(data)
        self.data = data