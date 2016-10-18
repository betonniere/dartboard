from browser import console

#----------------------------------
class Player :
    # ----
    def __init__ (self, name):
        self.name = name

#----------------------------------
class Cricket :
    # ----
    def __init__ (self):
        self.players = []
        self.player_count = 4
        for i in range (1, self.player_count+1):
            player = Player ('Player' + str (i))
            self.addPlayer (player)

        self.current_player = 0
        self.hit_count      = 0

    # ----
    def onHit (self, point, power):
        console.log ("===> " + self.players[self.current_player].name)
        self.hit_count += 1
        if self.hit_count == 3:
            self.togglePlayer ()

    # ----
    def addPlayer (self, player):
        self.players.append (player)

    # ----
    def togglePlayer (self):
        self.hit_count = 0
        self.current_player += 1
        self.current_player = self.current_player % self.player_count
