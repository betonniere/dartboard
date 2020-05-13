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

import serial
import time
from Queue     import Queue
from threading import Thread

grid_map = {
        '1.1': '"number":1,  "power":1',
        '1.2': '"number":1,  "power":2',
        '1.3': '"number":1,  "power":3',
        '1.4': '"number":2,  "power":1',
        '1.5': '"number":2,  "power":2',
        '1.6': '"number":2,  "power":3',
        '1.7': '"number":3,  "power":1',
        '1.8': '"number":3,  "power":2',
        '2.1': '"number":3,  "power":3',
        '2.2': '"number":4,  "power":1',
        '2.3': '"number":4,  "power":2',
        '2.4': '"number":4,  "power":3',
        '2.5': '"number":5,  "power":1',
        '2.6': '"number":5,  "power":2',
        '2.7': '"number":5,  "power":3',
        '2.8': '"number":6,  "power":1',
        '3.1': '"number":6,  "power":2',
        '3.2': '"number":6,  "power":3',
        '3.3': '"number":7,  "power":1',
        '3.4': '"number":7,  "power":2',
        '3.5': '"number":7,  "power":3',
        '3.6': '"number":8,  "power":1',
        '3.7': '"number":8,  "power":2',
        '3.8': '"number":8,  "power":3',
        '4.1': '"number":9,  "power":1',
        '4.2': '"number":9,  "power":2',
        '4.3': '"number":9,  "power":3',
        '4.4': '"number":10, "power":1',
        '4.5': '"number":10, "power":2',
        '4.6': '"number":10, "power":3',
        '4.7': '"number":11, "power":1',
        '4.8': '"number":11, "power":2',
        '5.1': '"number":11, "power":3',
        '5.2': '"number":12, "power":1',
        '5.3': '"number":12, "power":2',
        '5.4': '"number":12, "power":3',
        '5.5': '"number":13, "power":1',
        '5.6': '"number":13, "power":2',
        '5.7': '"number":13, "power":3',
        '5.8': '"number":14, "power":1',
        '6.1': '"number":14, "power":2',
        '6.2': '"number":14, "power":3',
        '6.3': '"number":15, "power":1',
        '6.4': '"number":15, "power":2',
        '6.5': '"number":15, "power":3',
        '6.6': '"number":16, "power":1',
        '6.7': '"number":16, "power":2',
        '6.8': '"number":16, "power":3',
        '7.1': '"number":17, "power":1',
        '7.2': '"number":17, "power":2',
        '7.3': '"number":17, "power":3',
        '7.4': '"number":18, "power":1',
        '7.5': '"number":18, "power":2',
        '7.6': '"number":18, "power":3',
        '7.7': '"number":19, "power":1',
        '7.8': '"number":19, "power":2',
        '8.1': '"number":19, "power":3',
        '8.2': '"number":20, "power":1',
        '8.3': '"number":20, "power":2',
        '8.4': '"number":20, "power":3',
        '8.5': '"number":25, "power":1',
        '8.6': '"number":25, "power":2',
        '8.7': '"number":0,  "power":0',
        '8.8': '"number":0,  "power":0'}

class SerialSniffer (Thread):
    # --------------------------------------------
    def __init__ (self, spawner, on_sniffer_data, fake):
        if fake:
            Thread.__init__ (self, target=self.fake_looper)
        else:
            Thread.__init__ (self, target=self.looper)

        self.sniffer_queue   = Queue ()
        self.spawner         = spawner
        self.on_sniffer_data = on_sniffer_data

    # --------------------------------------------
    def stop (self):
        self.sniffer_queue.put ("STOP")

    # --------------------------------------------
    def fake_looper (self):
        sector = 0
        power  = 0
        while True:
            self.spawner.spawn_callback (self.on_sniffer_data,
                                         '"number": ' + str (sector + 1) + ', "power": ' + str (power + 1) + '')
            sector += 1
            sector = sector%20
            power  += 1
            power  = power%3

            if not self.sniffer_queue.empty ():
                data = self.sniffer_queue.get ()
                if data == "STOP":
                    return

            time.sleep (1)

    # --------------------------------------------
    def looper (self):
        try:
            self.sp = serial.Serial ('/dev/ttyACM0', 9600, timeout=1)
        except serial.SerialException as e:
            print e
            return

        self.sp.flushInput ()

        while True:
            if not self.sniffer_queue.empty ():
                data = self.sniffer_queue.get ()
                if data == "STOP":
                    self.sp.close ()
                    return

            msg = self.sp.readline ()
            if msg != '':
                msg = msg.strip ('\n')
                msg = msg.strip ('\r')
                if (grid_map.has_key (msg)):
                    print msg + ' ==> ' + grid_map[msg]
                    self.on_sniffer_data (grid_map[msg])
