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
import os


# ----------------------------------
class ScoreBoard:
    # ----
    def __init__(self, json_scoreboard=None):
        if json_scoreboard is None:
            self.locks = {15: 3, 16: 3, 17: 3, 18: 3, 19: 3, 20: 3, 25: 3}
        else:
            self.locks = {}
            json_locks = json_scoreboard['locks']
            for key in json_locks:
                self.locks[int(key)] = json_locks[key]

    # ----
    def record_points(self, number, power):
        points = 0
        if number in self.locks:
            for _ in range(0, power):
                if self.locks[number] > 0:
                    self.locks[number] -= 1
                else:
                    points += 1

        return points

    # ----
    def number_closed(self, number):
        return self.locks[number] > 0

    # ----
    def completed(self):
        for lock in self.locks.values():
            if lock > 0:
                return False

        return True


# ----------------------------------
class Player:
    # ----
    def __init__(self, json_player=None):
        if json_player:
            self.name       = json_player['name']
            self.darts_used = json_player['darts_used']
            self.score      = json_player['score']
            self.thrower    = json_player['thrower']
            self.scoreboard = ScoreBoard(json_player['scoreboard'])
        else:
            self.name = None
            self.reset()

    # ----
    def reset(self):
        self.darts_used = 0
        self.score      = 0
        self.thrower    = False
        self.scoreboard = ScoreBoard()

    # ----
    def set_name(self, name):
        self.name = name

    # ----
    def out_of_darts(self):
        return self.darts_used >= 3

    # ----
    def release_dartboard(self):
        self.thrower = False

    # ----
    def reserve_dartboard(self):
        self.darts_used = 0
        self.thrower = True

    # ----
    def on_hit(self, number, power, competitors):
        if self.game_achieved(competitors) or self.out_of_darts():
            return

        points = self.scoreboard.record_points(number, power)
        self.darts_used += 1

        if points > 0:
            for c in competitors:
                if (c is not self) and (c.scoreboard.number_closed(number)):
                    self.score += number * points
                    break

        if self.game_achieved(competitors):
            self.darts_used = 3

    # ----
    def game_achieved(self, competitors):
        if (self.scoreboard.completed()):
            for c in competitors:
                if (c is not self) and (self.score < c.score):
                    return False
            return True

        return False


# ----------------------------------
class Cricket:
    # ----
    def __init__(self):
        self.recovery_path = os.getcwd() + '/games/cricket.json'
        self.players      = []
        self.rankings     = []
        self.current      = None
        self.iterator     = None
        self.rounds_to_go = 0

        if os.path.isfile(self.recovery_path):
            with open(self.recovery_path, 'r') as recovery_file:
                game = json.load(recovery_file)

                try:
                    self.rounds_to_go = game['rounds_to_go']
                    self.players = [Player(p) for p in game.get('players', [])]
                    self.rankings = [Player(p) for p in game.get('rankings', [])]
                except:
                    self.create_default()
                    return

                self.iterator = iter(self.players)
                for self.current in self.iterator:
                    if self.current.thrower:
                        break
        else:
            self.create_default()

    # ----
    def create_default(self):
        for _ in range(2):
            self.add_player()

        self.reset()

    # ----
    def on_hit(self, number, power):
        player = self.current
        if player:
            player.on_hit(number, power, self.players)

    # ----
    def give_rank(self, player):
        self.rankings.append(player)
        self.players.remove(player)

    # ----
    def started(self):
        if len(self.players) == 0:
            return False
        elif self.rounds_to_go < 20:
            return True
        if self.current != self.players[0]:
            return True
        if self.current.darts_used > 0:
            return True

        return False

    # ----
    def add_player(self, player=None):
        if self.rounds_to_go < 20:
            return False

        if len(self.players) >= 0 and len(self.players) < 8:
            if player is None:
                player = Player()
                player.set_name('P' + str(len(self.players) + 1))
            self.players.append(player)
            return True

        return False

    # ----
    def remove_player(self):
        if self.started():
            return False

        if len(self.players) > 1:
            self.players.pop()
            return True

        return False

    # ----
    def next_player(self, competitors):
        if len(self.players) == 0:
            return False

        player = self.current
        next_player = self.toggle_player()

        if player.game_achieved(competitors):
            self.give_rank(player)

        if len(self.players) == 1:
            self.give_rank(next_player)
        else:
            self.start_round(next_player)

        return True

    # ----
    def start_round(self, at=None):
        if self.rounds_to_go == 0:
            self.players = sorted(self.players, key=lambda player: player.score)
            while len(self.players) > 0:
                self.give_rank(self.players[0])
        else:
            self.iterator = iter(self.players)
            self.current  = next(self.iterator, None)
            if self.current:
                if at:
                    while self.current != at:
                        self.current = next(self.iterator)

                self.current.reserve_dartboard()

    # ----
    def toggle_player(self):
        try:
            self.current.release_dartboard()

            self.current = next(self.iterator)
            self.current.reserve_dartboard()
        except StopIteration:
            self.rounds_to_go -= 1
            self.start_round()

        return self.current

    # ----
    def screenshot(self):
        players = json.dumps(self.players, default=lambda o: o.__dict__, indent=4)
        rankings = json.dumps(self.rankings, default=lambda o: o.__dict__, indent=4)
        image  = '{\n'
        image += '"rounds_to_go": ' + str(self.rounds_to_go) + ',\n'
        image += '"players": ' + players + ',\n'
        image += '"rankings": ' + rankings + '\n'
        image += '}'

        with open(self.recovery_path, 'w') as recovery_file:
            recovery_file.write(image)

        return image

    # ----
    def reset(self):
        self.rounds_to_go = 20
        self.players = self.players + self.rankings
        self.players = sorted(self.players, key=lambda player: player.name)
        self.rankings = []

        for player in self.players:
            player.reset()

        self.start_round()

    # ----
    def on_message(self, msg):
        if msg['name'] == 'RESET':
            self.reset()
            return True
        elif msg['name'] == 'ADD_PLAYER':
            return self.add_player()
        elif msg['name'] == 'REMOVE_PLAYER':
            return self.remove_player()

        return False
