# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""
Displays a locations current, day min and max temperature, and the UV index.

Requires the following python packages:
    * requests

Parameters:
    * weather-uv.lat: Set current location latitude. Defualts to -41.286461.
    * weather-uv.lon: Set current location longitude. Defualts to 174.776230
    * weather-uv.apikey: API key from http://api.openweathermap.org


contributed by `yohanderose <https://github.com/yohanderose/>`
based on work from `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`
"""

import core.module
import core.widget
import core.input

import util.format
import util.location

import re
import time

import requests
from requests.exceptions import RequestException


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__temperature = 0
        self.__apikey = self.parameter(
            "apikey", "af7bfe22287c652d032a3064ffa44088")
        self.__icon = '🌤'
        self.__unit = 'metric'
        self.__valid = False

        self.__lat = self.parameter('lat', -41.28)
        self.__lon = self.parameter('lon', 174.77)

    def temperature(self):
        return util.format.astemperature(self.__feels_like, self.__unit)

    def tempmin(self):
        return util.format.astemperature(self.__tempmin, self.__unit)

    def tempmax(self):
        return util.format.astemperature(self.__tempmax, self.__unit)

    def output(self, widget):
        if not self.__valid:
            return f'Error: Weather unavailable'
        return f'{self.__icon} {self.temperature()} [{self.__tempmin}, {self.__tempmax}] UVI:{self.__uvi}'

    def update(self):
        """
        Update the weather information from openweathermap.org API
        """

        with open('/tmp/weather.log', 'a+') as f:
            log_str = ''
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n')

            try:
                url = f"https://api.openweathermap.org/data/2.5/onecall?lat={self.__lat}&lon={self.__lon}&units=metric&exclude=hourly&appid={self.__apikey}"

                res = requests.get(url)
                data = res.json()
                self.__city = data['timezone']
                self.__temperature = float(data['current']['temp'])
                self.__feels_like = float(data['current']['feels_like'])
                self.__tempmin = round(data['daily'][0]['temp']['min'])
                self.__tempmax = round(data['daily'][0]['temp']['max'])
                self.__weather = data['current']['weather'][0]['description'].lower(
                )
                self.__uvi = round(data['current']['uvi'])
                log_str = f'{self.__icon} {self.temperature()} [{self.__tempmin}, {self.__tempmax}] UVI:{self.__uvi}'
                self.__valid = True
            except Exception as e:
                log_str = str(e)
                self.__valid = False

            f.write(log_str + '\n')
            f.write('-' * 80 + '\n')
