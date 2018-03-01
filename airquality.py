#!/usr/bin/python
# -*- coding: utf-8 -*--

import sys
import re
from random import *
from threading import Timer
import requests
from bs4 import BeautifulSoup
from numpy import interp
import time


NOX = [0, 1]
NO = [2, 3]
NO2 = [4, 5]
NO2YLM = 40.0
NO215LM = 200.0

AREAS = {'Wells Rd': '1003', 'Bristol Depot': '1004', 'Parson St': '1005', 'Fishponds': '1010'}
URL = "http://www.bristol.airqualitydata.com/cgi-bin/currentreadings.cgi?aq&"
SITEURL = "http://www.bristol.airqualitydata.com/cgi-bin/sites.cgi?"
GRAPHURL = "http://www.bristol.airqualitydata.com/cgi-bin/graphs.cgi"

SAMPLE_TIME = 0


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def get_air_quality(area='Wells Rd'):
    url = URL
    url += AREAS[area]

    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")

    # readings have the units µg/m3
    get_air_quality.readings = soup.find_all(text=re.compile('µg/m3'))

    values = [float(x.split()[0]) for x in get_air_quality.readings if isinstance(x.split()[0], float)]

    return values


def get_air_dict(area='WellsRd', test=False):
    error = 0

    if test:
        values = [randint(1, 150), randint(1, 150), randint(1, 150), randint(1, 150), randint(1, 150), randint(1, 150)]
    else:
        values = get_air_quality(area)

    if len(values) < 6:
        values = [0] * 6
        error = 1

    return {'NOx15m': values[NOX[0]],
            'NOx24h': values[NOX[1]],
            'NO215m': values[NO2[0]],
            'NO224h': values[NO2[1]],
            'NO15m': values[NO[0]],
            'NO24h': values[NO[1]],
            'time': time.time(),
            'error': error}


def get_zeros():
    values = [0] * 6
    error = 1

    return {'NOx15m': values[NOX[0]],
            'NOx24h': values[NOX[1]],
            'NO215m': values[NO2[0]],
            'NO224h': values[NO2[1]],
            'NO15m': values[NO[0]],
            'NO24h': values[NO[1]],
            'time': time.time(),
            'error': error}


def display_air_quality():
    print("Getting air quality NO2 levels at Three Lamps Junction...")
    air_data = get_air_quality()
    print(air_data)
    n02now = air_data[NO2[0]]
    n02day = air_data[NO2[1]]
    print("Current 15 minute average N02 levels: " + str(n02now) + " ug/m3")
    print("Highest 15 minute average N02 levels in 24 hour window: " +
          str(n02day) + " ug/m3")

    maped = interp(n02now, [0, 40], [0, 84])

    if n02now > NO2YLM:
        print("Current levels trending above year mean legal limit of " + str(NO2YLM) + " ug/m3 !!")
    if n02day > NO215LM:
        print("Highest day value above legal limit of " + str(NO215LM) + " ug/m3 !!")


def main():
    main_task = RepeatedTimer(60 * 15, display_air_quality())

    while True:
        input(
            "Updating air quality data every 15 minutes, press [ENTER] key to quit")
        main_task.stop()
        sys.exit()
