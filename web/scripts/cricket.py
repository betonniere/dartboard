from browser import console

#----------------------------------
class ScoreBoard:
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
        return self.locks[number] < 3


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
                    if c.scoreboard.isLockedFor (number):
                        self.score += number*scored
                        break

    # ----
    def draw (self, ctx):
        ctx.font         = 'bold 3pt sans-serif'
        ctx.fillStyle    = 'green'
        ctx.textAlign    = 'left'
        ctx.textBaseline = 'middle'

        ctx.fillText (self.name + ' ' + str (self.score),
                      0,
                      0)


#----------------------------------
class Cricket:
    # ----
    def __init__ (self):
        self.players = []
        self.player_count = 2
        for p in range (1, self.player_count+1):
            player = Player ('Player' + str (p))
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
        for p in self.players:
            ctx.translate (0, 10)
            p.draw (ctx)
