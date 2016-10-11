import serial
import time
from Queue     import Queue
from threading import Thread

class SerialSniffer (Thread):
    # --------------------------------------------
    def __init__ (self, spawner, on_sniffer_data):
        Thread.__init__ (self, target=self.looper)

        self.sniffer_queue   = Queue ()
        self.spawner         = spawner
        self.on_sniffer_data = on_sniffer_data
        #self.sp = serial.Serial ('/dev/ttyACM0', 9600, timeout=1)

    # --------------------------------------------
    def stop (self):
        self.sniffer_queue.put ("STOP")
        #self.sp.close ()

    # --------------------------------------------
    def readSerial (self):
        return self.sp.readline().replace("\n", "")

    # --------------------------------------------
    def looper (self):
        #self.sp.flushInput ()

        sector = 0
        power  = 0
        while True:
            self.spawner.spawn_callback (self.on_sniffer_data,
                                         str (sector + 1) + '.' + str (power + 1))
            sector += 1
            sector = sector%20
            power  += 1
            power  = power%3
            time.sleep (1)

            if not self.sniffer_queue.empty ():
                data = self.sniffer_queue.get ()
                if data == "STOP":
                    return

            #if (self.sp.inWaiting () > 0):
                #data = self.readSerial ()
                #print "<< " + data + " >> sent to Tornado"
                #self.on_sniffer_data (data)
