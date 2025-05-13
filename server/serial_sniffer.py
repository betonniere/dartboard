# Copyright (C) Yannick Le Roux.
# This file is part of Dartboard.
#
#   Dartboard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dartboard is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Dartboard.  If not, see <http://www.gnu.org/licenses/>.

import queue
import re
import rich
import serial
import threading


# ----------------------------------
class SerialSniffer(threading.Thread):
    # ----
    def __init__(self, on_sniffer_data, context, device):
        threading.Thread.__init__(self, target=self.looper)

        self.sniffer_queue   = queue.Queue()
        self.context         = context
        self.on_sniffer_data = on_sniffer_data
        self.device          = device

    # ----
    def stop(self):
        self.sniffer_queue.put("STOP")

    # ----
    def looper(self):
        try:
            self.sp = serial.Serial('/dev/' + self.device, 115200, timeout=1)
        except serial.SerialException as e:
            rich.print(e)
            return

        self.sp.flushInput()

        hit_pattern = re.compile(r'^(?P<NUMBER>(\d{1,2}))X(?P<RATING>(\d))$')
        function_pattern = re.compile(r'^F(?P<NUMBER>(\d{1,2}))$')

        while True:
            if not self.sniffer_queue.empty():
                data = self.sniffer_queue.get()
                if data == "STOP":
                    self.sp.close()
                    return

            msg = self.sp.readline()
            if msg != '':
                msg = msg.decode('utf-8').strip()

                match = hit_pattern.match(msg)
                if match:
                    self.on_sniffer_data({'number': int(match.group('NUMBER')), 'power': int(match.group('RATING'))}, self.context)
                    continue

                match = function_pattern.match(msg)
                if match:
                    self.on_sniffer_data({'function': int(match.group('NUMBER'))}, self.context)
                    continue
