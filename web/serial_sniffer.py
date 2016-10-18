import serial
import time
from Queue     import Queue
from threading import Thread

grid_map = {'1.1': '1.1',
            '1.2': '1.2',
            '1.3': '1.3',
            '1.4': '2.1',
            '1.5': '2.2',
            '1.6': '2.3',
            '1.7': '3.1',
            '1.8': '3.2',
            '2.1': '3.3',
            '2.2': '4.1',
            '2.3': '4.2',
            '2.4': '4.3',
            '2.5': '5.1',
            '2.6': '5.2',
            '2.7': '5.3',
            '2.8': '6.1',
            '3.1': '6.2',
            '3.2': '6.3',
            '3.3': '7.1',
            '3.4': '7.2',
            '3.5': '7.3',
            '3.6': '8.1',
            '3.7': '8.2',
            '3.8': '8.3',
            '4.1': '9.1',
            '4.2': '9.2',
            '4.3': '9.3',
            '4.4': '10.1',
            '4.5': '10.2',
            '4.6': '10.3',
            '4.7': '11.1',
            '4.8': '11.2',
            '5.1': '11.3',
            '5.2': '12.1',
            '5.3': '12.2',
            '5.4': '12.3',
            '5.5': '13.1',
            '5.6': '13.2',
            '5.7': '13.3',
            '5.8': '14.1',
            '6.1': '14.2',
            '6.2': '14.3',
            '6.3': '15.1',
            '6.4': '15.2',
            '6.5': '15.3',
            '6.6': '16.1',
            '6.7': '16.2',
            '6.8': '16.3',
            '7.1': '17.1',
            '7.2': '17.2',
            '7.3': '17.3',
            '7.4': '18.1',
            '7.5': '18.2',
            '7.6': '18.3',
            '7.7': '19.1',
            '7.8': '19.2',
            '8.1': '19.3',
            '8.2': '20.1',
            '8.3': '20.2',
            '8.4': '20.3',
            '8.5': '25.1',
            '8.6': '25.2',
            '8.7': '0.0',
            '8.8': '0.0'}

class SerialSniffer (Thread):
    # --------------------------------------------
    def __init__ (self, spawner, on_sniffer_data):
        #Thread.__init__ (self, target=self.looper)
        Thread.__init__ (self, target=self.fake_looper)

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
