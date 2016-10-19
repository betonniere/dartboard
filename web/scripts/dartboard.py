from browser import document
from browser import html
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
        self.socket = None
        self.game   = game

        self.canvas = document['dartboard_canvas']
        self.ctx    = self.canvas.getContext ('2d')

        self.scratchpad  = html.CANVAS (width = self.canvas.width, height = self.canvas.height)
        self.scratch_ctx = self.scratchpad.getContext ('2d')

        self.ctx.drawImage (self.scratchpad, 0, 0)

    # ----
    def onSocketOpen (self, evt):
        pass

    # ----
    def onSocketMessage (self, msg):
        if msg.data == "HELLO":
            pass
        elif msg.data == "GOODBYE":
            alert (msg.data)
        else:
            param  = msg.data.split ('.')
            number = int (param[0])
            power  = int (param[1])

            self.game.onHit (number, power)
            self.draw (number, power)

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
    def draw (self, focus_number, focus_power):
        self.scratch_ctx.fillStyle = 'white'
        self.scratch_ctx.fillRect (0, 0, self.canvas.width, self.canvas.height)

        if (self.canvas.width <= self.canvas.height):
            size = self.canvas.width
        else:
            size = self.canvas.height

        self.scratch_ctx.save ()
        self.scratch_ctx.scale     (size/100, size/100)
        self.scratch_ctx.translate (100/2, 100/2)

        # Background
        self.scratch_ctx.arc (0, 0, 50, 0, 2*pi, False)
        self.scratch_ctx.fillStyle = 'black'
        self.scratch_ctx.fill   ()

        # Numbers
        self.scratch_ctx.font         = 'bold 3pt sans-serif'
        self.scratch_ctx.fillStyle    = 'White'
        self.scratch_ctx.textAlign    = 'center'
        self.scratch_ctx.textBaseline = 'middle'

        for i in range (1, 21):
            self.scratch_ctx.fillText (str (i),
                                       46*cos((i * 2*pi/20) - pi/2),
                                       46*sin((i * 2*pi/20) - pi/2))

        # Sectors
        self.scratch_ctx.save ()
        self.scratch_ctx.rotate (-pi/2 + 2*pi/20)
        self.scratch_ctx.strokeStyle = 'rgb(100,100,100)'

        # Big sectors
        for i in range (1, 21):
          sector = BigSector (i+1, Dartboard.safe_area)
          sector.draw (self.scratch_ctx, focus_number, focus_power)

        # Power sectors
        for power in range (2, 4):
            for i in range (1, 21):
                sector = SmallSector (i+1, Dartboard.safe_area, power, 3)
                sector.draw (self.scratch_ctx, focus_number, focus_power)

        self.scratch_ctx.restore ()

        # Bull's eye
        for power in range (1, 3):
            sector = BullSector (25*power, Dartboard.safe_area, power)
            sector.draw (self.scratch_ctx, focus_number, focus_power)

        self.scratch_ctx.save ()
        self.scratch_ctx.translate (-50, 55)
        self.game.draw (self.scratch_ctx)
        self.scratch_ctx.restore ()

        self.scratch_ctx.restore ()

        self.ctx.drawImage (self.scratchpad, 0, 0)



#----------------------------------
game = Cricket ()

dartboard = Dartboard (game)
dartboard.openSocket ()
dartboard.draw (99, 99)
