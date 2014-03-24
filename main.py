__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'


from powermon.powermon import *
from powermon.cmdformat import CmdTx_Calibrate_Request
from pydispatch import dispatcher
import datetime

def main():
    pm = PowerMon('COM28')
    pm.connect()

    # calibrate
    dt = datetime.datetime.now()
    calibrate_container = Container(
                year = dt.year - 2000,
                month = dt.month,
                date = dt.day,
                hours = dt.hour,
                minutes = dt.minute,
                seconds = dt.second,
                milliseconds = 0
            )
    resp = pm.send_cmd(CmdTx_Calibrate_Request, calibrate_container, expected_resp_cmd=CmdRx_Calibrate_Confirm)
    if resp.status != 0:
        return
    # enable burst mode
    enable_burst_container = Container()
    resp = pm.send_cmd(CmdTx_EnableBurst_Request, enable_burst_container, expected_resp_cmd=CmdRx_EnableBurst_Confirm)
    if resp.status != 0:
        return
    # register command handler
    dispatcher.connect(CmdRx_RmsChanged_Report_handler, signal='CmdRx_RmsChanged_Report', sender=dispatcher.Any)
    while True:
        pass

def CmdRx_RmsChanged_Report_handler(sender, cmd):
    dt = datetime.datetime(cmd.year + 2000, cmd.month, cmd.date, cmd.hours, cmd.minutes, cmd.seconds)
    print('%s - pu1 = %d, pu2 = %d, pu3 = %d' % (dt, cmd.pu1, cmd.pu2, cmd.pu3))

if __name__ == '__main__':
    main()