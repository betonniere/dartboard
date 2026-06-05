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
import subprocess
import threading


# ----------------------------------
class NetworkStatus(threading.Thread):
    # ----
    def __init__(self, on_network_status, context):
        super().__init__(target=self.looper)

        self.control_queue = queue.Queue()
        self.context = context
        self.on_network_status = on_network_status

    # ----
    def stop(self):
        self.control_queue.put('STOP')

    # ---
    def send_network_status(self):
        cmd = ['nmcli', '-g', 'NAME', 'connection', 'show', '--active']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            active_connections = result.stdout.strip().split()
            if active_connections:
                self.on_network_status(active_connections[0])

    # ----
    def looper(self):
        while True:
            try:
                data = self.control_queue.get(block=True, timeout=5)
                if data == 'STOP':
                    return
            except queue.Empty:
                self.send_network_status()
