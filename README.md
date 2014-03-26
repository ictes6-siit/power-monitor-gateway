=====================
power-monitor-gateway
=====================

Install setup tool
=================

    curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -o - | sudo python

Install program
===============

    sudo python setup.py install

Using program
==============

    powermon -i "/dev/ttyACM0"

    **Options**
        -i, --port : Serial port
        -b, --buad : Buad Rate
        -l, --loglevel : Logging level (e.g. 'debug', 'info', 'warning', 'error', 'critical')
        -f, --logfile : The log file to be write.