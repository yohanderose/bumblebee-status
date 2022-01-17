# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""
Given some day in the future, print out how many days, and hours until that day.

Parameters:
    * countdown.name (optional): The name of the event to countdown to.
    * countdown.date: The date of the event to countdown to in this style '5 July, 2022'


contributed by `yohanderose <https://github.com/yohanderose/>`
"""

import core.module
import core.widget
import core.input

import util.format
import util.location

import time


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__icon = '⏲'
        self.__date = self.parameter(
            'date', f'{time.time()}')
        self.__name = self.parameter(
            'name', 'countdown')
        self.__daysleft = 0
        self.__hoursleft = 0

    def get_remaining_days(self, date):
        """
        Get the number of days and hours until the given date.
        """
        now = time.time()
        then = time.mktime(time.strptime(date, "%d %B, %Y"))
        self.__daysleft = int((then - now) / (24 * 3600))
        self.__hoursleft = int((then - now) / 3600) % 24

    def output(self, widget):
        content = f'  {self.__icon} {self.__name}: {self.__daysleft} days, {self.__hoursleft} hours'
        return content
        # return [
        #     {
        #         'full_text': content,
        #         'color': self.theme.Color.Text,
        #         'separator': False,
        #         'separator_block_width': 0,
        #     }
        # ]

    def update(self):

        with open('/tmp/countdown.log', 'a') as f:
            log_str = ''
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n')

            try:
                self.get_remaining_days(self.__date)
                log_str = f'{self.__icon} {self.__name}: {self.__daysleft} days, {self.__hoursleft} hours'
            except Exception as e:
                log_str = str(e)

            f.write(log_str + '\n')
            f.write('-' * 80 + '\n')
