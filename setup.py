#!/usr/bin/env python

from setuptools import setup
import powermon


setup(
    name='power-monitor-gateway',
    version=powermon.__version__,
    description='Power Sensor access module',
    author='Ratchasak Ranron',
    author_email='ratchasak.ranron@gmail.com',
    license = 'None',
    url='',
    scripts=['tools/powermon'],
    packages=['powermon'],
    install_requires=['PyDispatcher==2.0.3',
                        'construct==2.5.1',
                        'pyserial==2.7'
                    ],
    long_description =
"""
power-monitor-gateway is the module to communicate with Power Sensor for getting the sensor data or config the sensor.
"""
)