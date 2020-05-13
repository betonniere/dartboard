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

import json

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
        return self.locks[number] > 0

#----------------------------------
class Player:
    # ----
    def __init__ (self, name):
        self.name       = name
        self.darts_used = 0
        self.score      = 0
        self.focus      = False
        self.scoreboard = ScoreBoard ()

    # ----
    def resetVolley (self):
        self.darts_used = 0

    # ----
    def volleyIsDone (self):
        return self.darts_used >= 3

    # ----
    def setFocus (self, focus):
        self.focus = focus

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
        self.current.setFocus (True)

    # ----
    def togglePlayer (self):
        try:
            self.current.resetVolley ()
            self.current.setFocus (False)

            self.current = next (self.iterator)
            self.current.setFocus (True)
        except StopIteration:
            self.startRound ()

    # ----
    def screenShot (self):
        return '"players": ' + json.dumps (self.players, default=lambda o: o.__dict__, indent=4)
