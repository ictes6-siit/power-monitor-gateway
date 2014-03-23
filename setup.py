#!/usr/bin/env python

from distutils.core import setup

import powermon


setup(
    name='power-monitor-gateway',
    version=powermon.__version__,
    description='Power Sensor access module',
    author='Ratchasak Ranron',
    author_email='ratchasak.ranron@gmail.com',
    license = 'None',
    url='',
    packages=['powermon'],
    long_description =
"""
power-monitor-gateway is the module to communicate with Power Sensor for getting the sensor data or config the sensor.
"""
)