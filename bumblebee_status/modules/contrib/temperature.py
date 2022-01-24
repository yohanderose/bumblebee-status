# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""
Displays the cpu temperature from acpi.

contributed by `yohanderose <https://github.com/yohanderose/>`
"""

import core.module
import core.widget
import core.input

import util.format
import util.location

import time
import subprocess


class Module(core.module.Module):
    @core.decorators.every(seconds=3)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__icon = '🌡'
        self.__temperature = 0
        self.__unit = 'metric'

    def temperature(self):
        return util.format.astemperature(self.__temperature, self.__unit)

    def output(self, widget):
        return f' {self.__icon} {self.temperature()}'

    def get_temp(self):
        cmd = 'acpi -t | cut -d " " -f 4'
        output = subprocess.check_output(
            cmd, shell=True).decode('utf-8')
        self.__temperature = float(output.strip())

    def update(self):
        """
        Update the weather information from openweathermap.org API
        """

        with open('/tmp/acpi-temp.log', 'a') as f:
            log_str = ''
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n')

            try:
                self.get_temp()
                log_str = f'{self.__icon} {self.temperature()}'
            except Exception as e:
                log_str = str(e)

            f.write(log_str + '\n')
            f.write('-' * 80 + '\n')
