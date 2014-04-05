power-monitor-gateway
=====================

Install setup tool
------------------

    curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -o - | sudo python

Install program
----------------

    sudo python setup.py install

Set real time
-------------
    
    sudo dpkg-reconfigure tzdata

Using program
-------------

    powermon -i "/dev/ttyACM0"

    Options
        -i, --port : Serial port e.g. "/dev/ttyACM0"
        -b, --buad : Buad Rate e.g. 152000
        -l, --loglevel : Logging level e.g. 'debug', 'info', 'warning', 'error', 'critical'
        -f, --logfile : The log file to be write. e.g. '/var/log/powermon.log
