from browser import document
from browser import alert
from browser import console
from browser import websocket
from math    import pi
from math    import sin
from math    import cos

from sector  import BigSector
from sector  import SmallSector
from sector  import BullSector

from cricket import Cricket

#----------------------------------
class Dartboard:
    safe_area = 8

    # ----
    def __init__ (self, game):
        self.canvas = document['dartboard_canvas']
        self.ctx    = self.canvas.getContext ('2d')
        self.socket = None
        self.game   = game

    # ----
    def onSocketOpen (self, evt):
        pass

    # ----
    def onSocketMessage (self, msg):
        if msg.data == "HELLO":
            pass
        elif msg.data == "GOODBYE":
            alert (msg.data);
        else:
            param = msg.data.split ('.');
            point = int (param[0])
            power = int (param[1]);

            self.game.onHit (point, power)
            self.draw (point, power)

    # ----
    def onSocketClose (self, evt):
        pass

    # ----
    def openSocket (self):
        if not websocket.supported:
            alert ('WebSocket is not supported by your browser')
            return

        self.socket = websocket.WebSocket ('ws://localhost:8080/websocket')
        self.socket.bind ('open',    self.onSocketOpen)
        self.socket.bind ('message', self.onSocketMessage)
        self.socket.bind ('close',   self.onSocketClose)

    # ----
    def draw (self, focus_point, focus_power):
        if (self.canvas.width <= self.canvas.height):
            size = self.canvas.width
        else:
            size = self.canvas.height

        self.ctx.save ()
        self.ctx.scale     (size/100, size/100)
        self.ctx.translate (100/2, 100/2)

        # Background
        self.ctx.arc (0, 0, 50, 0, 2*pi, False)
        self.ctx.fillStyle = 'black'
        self.ctx.fill   ()

        # Points
        self.ctx.font         = 'bold 3pt sans-serif'
        self.ctx.fillStyle    = 'White'
        self.ctx.textAlign    = 'center'
        self.ctx.textBaseline = 'middle'

        for i in range (1, 21):
            self.ctx.fillText (str (i),
                               46*cos((i * 2*pi/20) - pi/2),
                               46*sin((i * 2*pi/20) - pi/2))

        # Sectors
        self.ctx.save ()
        self.ctx.rotate (-pi/2 + 2*pi/20)
        self.ctx.strokeStyle = 'rgb(100,100,100)'

        # Big sectors
        for i in range (1, 21):
          sector = BigSector (i+1, Dartboard.safe_area)
          sector.draw (self.ctx, focus_point, focus_power)

        # Power sectors
        for power in range (2, 4):
            for i in range (1, 21):
                sector = SmallSector (i+1, Dartboard.safe_area, power, 3)
                sector.draw (self.ctx, focus_point, focus_power)

        self.ctx.restore ()

        # Bull's eye
        for power in range (1, 3):
            sector = BullSector (25*power, Dartboard.safe_area, power)
            sector.draw (self.ctx, focus_point, focus_power)

        self.ctx.restore ()


#----------------------------------
game = Cricket ()

dartboard = Dartboard (game)
dartboard.openSocket ()
dartboard.draw (99, 99)
