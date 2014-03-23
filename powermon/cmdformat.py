__author__ = 'Ratchasak Ranron <ratchasak.ranron@gmail.com>'

from construct import *

SYNC_BYTE = 0xAA

#========== Tx Command format
CmdTx_Calibrate_Request = \
    Struct("CmdTx_Calibrate_Request",
        ULInt8("year"),
        ULInt8("month"),
        ULInt8("date"),
        ULInt8("hours"),
        ULInt8("minutes"),
        ULInt8("seconds"),
        ULInt16("milliseconds"),
    )

CmdTx_EnableBurst_Request = \
    Struct("CmdTx_EnableBurst_Request",
    )

CmdTx_DisableBurst_Request = \
    Struct("CmdTx_DisableBurst_Request",
    )
#========== End Tx Command format

#========== Rx Command format

CmdRx_Calibrate_Confirm = \
    Struct("CmdRx_Calibrate_Confirm",
        Byte("status"),
    )

CmdRx_EnableBurst_Confirm = \
    Struct("CmdRx_EnableBurst_Confirm",
        Byte("status"),
    )

CmdRx_DisableBurst_Confirm = \
    Struct("CmdRx_DisableBurst_Confirm",
       Byte("status"),
    )

CmdRx_RmsChanged_Report = \
    Struct("CmdRx_RmsChanged_Report",
        Byte("status"),
        ULInt8("year"),
        ULInt8("month"),
        ULInt8("date"),
        ULInt8("hours"),
        ULInt8("minutes"),
        ULInt8("seconds"),
        ULInt16("milliseconds"),
        ULInt8("pu1"),
        ULInt8("pu2"),
        ULInt8("pu3"),
    )
#========== End Rx Command format

Cmd_Format = \
    Struct("cmd_format",
        Const(Byte("sync"), SYNC_BYTE),
        Enum(Byte("cmdType"),
            #Tx
            CmdTx_Calibrate_Request = 0xA0,
            CmdTx_EnableBurst_Request = 0xA1,
            CmdTx_DisableBurst_Request = 0xA2,

            # Rx
            CmdRx_Calibrate_Confirm = 0xB0,
            CmdRx_EnableBurst_Confirm = 0xB1,
            CmdRx_DisableBurst_Confirm = 0xB2,
            CmdRx_RmsChanged_Report = 0xC0,
        ),
        Byte("len"),
        #==== Bind data
        #Tx
        If(lambda ctx: ctx["cmdType"] == 'CmdTx_Calibrate_Request', Embed(CmdTx_Calibrate_Request)),
        If(lambda ctx: ctx["cmdType"] == 'CmdTx_EnableBurst_Request', Embed(CmdTx_EnableBurst_Request)),
        If(lambda ctx: ctx["cmdType"] == 'CmdTx_DisableBurst_Request', Embed(CmdTx_DisableBurst_Request)),
        #Rx
        If(lambda ctx: ctx["cmdType"] == 'CmdRx_Calibrate_Confirm', Embed(CmdRx_Calibrate_Confirm)),
        If(lambda ctx: ctx["cmdType"] == 'CmdRx_EnableBurst_Confirm', Embed(CmdRx_EnableBurst_Confirm)),
        If(lambda ctx: ctx["cmdType"] == 'CmdRx_DisableBurst_Confirm', Embed(CmdRx_DisableBurst_Confirm)),
        If(lambda ctx: ctx["cmdType"] == 'CmdRx_RmsChanged_Report', Embed(CmdRx_RmsChanged_Report)),
        #==== End bind data

        Byte("fcs")
    )
