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
import random
import rich
import serial
import threading
import time


# ----------------------------------
class SerialSniffer(threading.Thread):
    # ----
    def __init__(self, on_sniffer_data, context, fake, device):
        if fake:
            threading.Thread.__init__(self, target=self.fake_looper)
        else:
            threading.Thread.__init__(self, target=self.looper)

        self.sniffer_queue   = queue.Queue()
        self.context         = context
        self.on_sniffer_data = on_sniffer_data
        self.device          = device

    # ----
    def stop(self):
        self.sniffer_queue.put("STOP")

    # ----
    def fake_looper(self):
        sectors = list(range(15, 20 + 1)) + [25]
        while True:
            sector = sectors[random.randint(0, len(sectors)) - 1]
            if sector == 25:
                power = random.randint(1, 2)
            else:
                power = random.randint(1, 3)

            self.on_sniffer_data({'number': sector, 'power': power}, self.context)

            if not self.sniffer_queue.empty():
                data = self.sniffer_queue.get()
                if data == "STOP":
                    return

            time.sleep(1)

    # ----
    def looper(self):
        try:
            self.sp = serial.Serial('/dev/' + self.device, 115200, timeout=1)
        except serial.SerialException as e:
            rich.print(e)
            return

        self.sp.flushInput()

        pattern = re.compile(r'^(?P<NUMBER>(\d{1,2}))X(?P<RATING>(\d))$')

        while True:
            if not self.sniffer_queue.empty():
                data = self.sniffer_queue.get()
                if data == "STOP":
                    self.sp.close()
                    return

            msg = self.sp.readline()
            if msg != '':
                msg = msg.decode('utf-8').strip()
                match = pattern.match(msg)
                if match:
                    self.on_sniffer_data({'number': int(match.group('NUMBER')), 'power': int(match.group('RATING'))}, self.context)
