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

import os
import json

#----------------------------------
class ScoreBoard:
    # ----
    def __init__ (self, json_scoreboard=None):
        if json_scoreboard is None:
            self.locks = {15:3, 16:3, 17:3, 18:3, 19:3, 20:3}
        else:
            self.locks = {}
            json_locks = json_scoreboard['locks']
            for key in json_locks:
                self.locks[int (key)] = json_locks[key]

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
    def __init__ (self, json_player=None):
        if json_player is None:
            self.name       = None
            self.darts_used = 0
            self.score      = 0
            self.focus      = False
            self.scoreboard = ScoreBoard ()
        else:
            self.name       = json_player['name']
            self.darts_used = json_player['darts_used']
            self.score      = json_player['score']
            self.focus      = json_player['focus']
            self.scoreboard = ScoreBoard (json_player['scoreboard'])

    # ----
    def setName (self, name):
        self.name = name

    # ----
    def resetVolley (self):
        self.darts_used = 0

    # ----
    def volleyIsDone (self):
        return self.darts_used >= 3

    # ----
    def hasFocus (self):
        return self.focus

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
        self.recovery_path = cwd = os.getcwd () + '/cricket.recovery'
        self.players       = []
        self.current       = None
        self.iterator      = None

        if os.path.isfile (self.recovery_path):
            with open (self.recovery_path, 'r') as recovery_file:
                game = json.load (recovery_file)
                for json_player in game['players']:
                    player = Player (json_player)
                    self.addPlayer (player)

                self.iterator = iter (self.players)
                for self.current in self.iterator:
                    if self.current.hasFocus ():
                        break;
        else:
            for p in range (0, 2):
                player = Player ()
                player.setName ('P' + str (p+1))
                self.addPlayer (player)

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
        self.current  = next (self.iterator, None)
        if self.current:
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
        image = '"players": ' + json.dumps (self.players, default=lambda o: o.__dict__, indent=4)

        with open (self.recovery_path, 'w') as recovery_file:
            recovery_file.write ('{' + image + '}');

        return image
