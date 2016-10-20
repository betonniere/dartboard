from browser import console
from browser import html

#----------------------------------
class ScoreBoard:
    lock_images = {0:'3.png', 1:'2.png', 2:'1.png', 3:'0.png'}

    # ----
    def __init__ (self):
        self.locks = {15:3, 16:3, 17:3, 18:3, 19:3, 20:3}

    # ----
    def removeLock (self, number, power):
        score = 0
        if number in self.locks:
            for i in range (0, power):
                if self.locks[number] > 0:
                    self.locks[number] -= 1
                else:
                    score += 1

        return score

    # ----
    def isLockedFor (self, number):
        return self.locks[number] > 0

    # ----
    def draw (self, ctx, competitors):
        ctx.save ()

        for number in self.locks:
            ctx.translate (8, 0)

            for c in competitors:
                if c.scoreboard.isLockedFor (number):
                    ctx.save ()
                    ctx.scale (0.5, 0.5)
                    image       = html.IMG ()
                    image.src   = ScoreBoard.lock_images[self.locks[number]]
                    ctx.drawImage (image, 0, -10)
                    ctx.restore ()

        ctx.restore ()


#----------------------------------
class Player:
    # ----
    def __init__ (self, name):
        self.name       = name
        self.darts_used = 0
        self.score      = 0
        self.scoreboard = ScoreBoard ()

    # ----
    def resetVolley (self):
        self.darts_used = 0

    # ----
    def volleyIsDone (self):
        return self.darts_used >= 3

    # ----
    def onHit (self, number, power, competitors):
        if not self.volleyIsDone ():
            scored = self.scoreboard.removeLock (number, power)
            self.darts_used += 1

            if scored > 0:
                for c in competitors:
                    if (c is not self) and (c.scoreboard.isLockedFor (number)):
                        self.score += number*scored
                        break

    # ----
    def draw (self, ctx, competitors):
        ctx.save ()
        ctx.font         = 'bold 5pt sans-serif'
        ctx.fillStyle    = 'black'
        ctx.textAlign    = 'left'
        ctx.textBaseline = 'middle'

        ctx.fillText (self.name,
                      0,
                      0)
        ctx.translate (7, 0)
        self.scoreboard.draw (ctx, competitors)
        ctx.restore ()

        ctx.save ()
        ctx.font         = 'bold 7pt sans-serif'
        ctx.fillStyle    = 'black'
        ctx.textAlign    = 'right'
        ctx.translate (97, 0)
        ctx.fillText (str (self.score),
                      0,
                      0)
        ctx.restore ()


#----------------------------------
class Cricket:
    # ----
    def __init__ (self):
        self.players = []
        self.player_count = 2
        for p in range (1, self.player_count+1):
            player = Player ('P' + str (p))
            self.addPlayer (player)

        self.current  = None
        self.iterator = None
        self.startRound ()

    # ----
    def onHit (self, number, power):
        self.current.onHit (number, power, self.players)

        if self.current.volleyIsDone ():
            self.togglePlayer ()

    # ----
    def addPlayer (self, player):
        self.players.append (player)

    # ----
    def startRound (self):
        self.iterator = iter (self.players)
        self.current  = next (self.iterator)

    # ----
    def togglePlayer (self):
        try:
            self.current.resetVolley ()
            self.current = next (self.iterator)
        except StopIteration:
            self.startRound ()

    # ----
    def draw (self, ctx):
        spacing = 14
        ctx.save ()

        ctx.translate (0, spacing/1.5)
        if len (self.players) >= 1:
            ctx.save ()
            ctx.translate (7+8+2, 0)
            for l in self.players[1].scoreboard.locks:
                ctx.font         = 'bold 3pt sans-serif'
                ctx.fillStyle    = 'darkblue'
                ctx.textAlign    = 'center'
                ctx.textBaseline = 'middle'

                ctx.fillText (str (l),
                              0,
                              0)
                ctx.translate (8, 0)
            ctx.restore ()

            ctx.translate (0, spacing/1.5)

        for p in self.players:
            if p is self.current:
                ctx.fillStyle = 'lightgrey'
                ctx.fillRect (0, -spacing/2, 100, spacing)

            p.draw (ctx, self.players)
            ctx.translate (0, spacing)

        ctx.restore ()
