import serial
import time
from Queue     import Queue
from threading import Thread

grid_map = {'0.0': '1.1',
            '0.1': '1.2',
            '0.2': '1.3',
            '0.3': '2.1',
            '0.4': '2.2',
            '0.5': '2.3',
            '0.6': '3.1',
            '0.7': '3.2',
            '0.8': '3.3',
            '1.0': '4.1',
            '1.1': '4.2',
            '1.2': '4.3',
            '1.3': '5.1',
            '1.4': '5.2',
            '1.5': '5.3',
            '1.6': '6.1',
            '1.7': '6.2',
            '2.0': '6.3',
            '2.1': '7.1',
            '2.2': '7.2',
            '2.3': '7.3',
            '2.4': '8.1',
            '2.5': '8.2',
            '2.6': '8.3',
            '2.7': '9.1',
            '3.0': '9.2',
            '3.1': '9.3',
            '3.2': '10.1',
            '3.3': '10.2',
            '3.4': '10.3',
            '3.5': '11.1',
            '3.6': '11.2',
            '3.7': '11.3',
            '4.0': '12.1',
            '4.1': '12.2',
            '4.2': '12.3',
            '4.3': '13.1',
            '4.4': '13.2',
            '4.5': '13.3',
            '4.6': '14.1',
            '4.7': '14.2',
            '5.0': '14.3',
            '5.1': '15.1',
            '5.2': '15.2',
            '5.3': '15.3',
            '5.4': '16.1',
            '5.5': '16.2',
            '5.6': '16.3',
            '5.7': '17.1',
            '6.0': '17.2',
            '6.1': '17.3',
            '6.2': '18.1',
            '6.3': '18.2',
            '6.4': '18.3',
            '6.5': '19.1',
            '6.6': '19.2',
            '6.7': '19.3',
            '7.0': '20.1',
            '7.1': '20.2',
            '7.2': '20.3',
            '7.3': 'B.1',
            '7.4': 'B.2',
            '7.5': '0.0',
            '7.6': '0.0',
            '7.7': '0.0'}

class SerialSniffer (Thread):
    # --------------------------------------------
    def __init__ (self, spawner, on_sniffer_data):
        Thread.__init__ (self, target=self.looper)
        #Thread.__init__ (self, target=self.fake_looper)

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
        time.sleep (5)
        while True:
            self.spawner.spawn_callback (self.on_sniffer_data,
                                         str (sector + 1) + '.' + str (power + 1))
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
        self.sp = serial.Serial ('/dev/ttyACM0', 9600, timeout=1)
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
