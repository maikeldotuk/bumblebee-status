# pylint: disable=C0111,R0903

"""Displays CPU utilization across all CPUs.

Parameters:
    * cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
    * cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
"""

import psutil
import bumblebee.input
import bumblebee.output
import bumblebee.engine
import requests
import datetime

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.utilization)
        )
        self.value = 'Fuck you'
        self.conversion = 0
        self.thehour = 99
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="gnome-system-monitor")

    def utilization(self, widget):
        r = requests.get('https://minexmr.com/api/pool/stats_address?address=85vYynqvPErawpSiVtjd1SAC1Tw7gA3npQckm8zmk66b5PXEnVM3cYeVd9VFLxJLrK96qj5BtcxMfNF1349s6qGvVZWrjTF&longpoll=false')
        to_json = r.json()
        result = to_json["stats"]["balance"]
        multiplier_unit = 0.000000000001
        to_decimal = int(result) * multiplier_unit
        conversion = self.fetchconversion()
        end_result = "{0:.2f}".format(to_decimal * conversion)
        end_xmr = "{0:.4f}".format(to_decimal)
        return u"\xA3" + str(end_result) + ' ' + u"\u0271" + end_xmr

    def fetchconversion(self):
        # TODO: This should be done differently, to allow for different currency
        # Should get it just once per hour
        rightnow = datetime.datetime.now().hour
        if self.thehour == rightnow:
            return self.conversion
        else:
            r = requests.get('https://api.cryptonator.com/api/ticker/xmr-gbp')
            try:
                to_json = r.json()
                result = to_json['ticker']['price']
                to_decimal = float(result)
                self.conversion = to_decimal
                self.thehour = rightnow
            except Exception as e:
                return self.conversion
            return to_decimal

    def update(self, widgets):
        self.value = 'Fuck you again'

    def state(self, widget):
        meh = 10
        return self.threshold_state(meh, 70, 80)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
