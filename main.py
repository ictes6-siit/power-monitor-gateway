__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'


from powermon.powermon import *
from powermon.cmdformat import CmdTx_Calibrate_Request

def main():
    pm = PowerMon('COM1')
    pm.connect()

    cmd_container = Container(
                year = 1,
                month = 1,
                date = 1,
                hours = 1,
                minutes = 1,
                seconds = 1,
                milliseconds = 2
            )
    resp = pm.write(CmdTx_Calibrate_Request, cmd_container, expected_resp_cmd=CmdRx_Calibrate_Confirm)
    print('Response : ', resp)
    while True:
        pass


if __name__ == '__main__':
    main()