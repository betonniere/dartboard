// Copyright (C) Yannick Le Roux.
// This file is part of Dartboard.
//
//   Dartboard is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   Dartboard is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with Dartboard.  If not, see <http://www.gnu.org/licenses/>.

class GamePanel extends Panel
{
  static nb_lock_images = 4;
  static lock_images = {};
  static images = {'dart': null, 'podium': null};

  static images_to_load = 0;

  // ----
  constructor (scratchpad, socket, listener)
  {
    super (scratchpad, socket, listener);
  }

  // ----
  plug ()
  {
    if (Object.keys (GamePanel.lock_images).length == 0)
    {
      let caller = this;

      GamePanel.images_to_load = Object.keys(GamePanel.images).length + GamePanel.nb_lock_images;

      for (const i in GamePanel.images)
      {
        let image = new Image ();

        image.src    = i + '.svg';
        image.onload = function () {GamePanel.images[i] = image; caller.onImageloaded (image)};
      }

      for (let i = 0; i < GamePanel.nb_lock_images; i++)
      {
        let image = new Image ();

        image.src    =  i + '.svg';
        image.onload = function () {GamePanel.lock_images[i] = image; caller.onImageloaded (image)};
      }
    }
  }

  // ----
  onImageloaded (image)
  {
    GamePanel.images_to_load--;
    if (GamePanel.images_to_load == 0)
    {
      this.listener.onPanelReady ();
    }
  }

  // ----
  draw (data)
  {
    let spacing_small = 7;
    let spacing_big   = 2*spacing_small;
    let thrower       = null;

    this.startDrawing ();
    {
      let players;
      let game_over = (data['players'].length == 0) && (data['rankings'].length > 0);

      this.scratchpad.fillStyle = '#800000';
      this.scratchpad.fillRect (0, 0, 100, 100);

      this.scratchpad.translate (spacing_small, spacing_small);

      if (game_over)
      {
        players = data['rankings'].reverse();
      }
      else
      {
        players = data['players'];

        // Header
        this.scratchpad.save ();
        {
          this.scratchpad.translate (spacing_small, 0);
          this.scratchpad.translate (spacing_small, 0);

          for (let lock in players[0].scoreboard.locks)
          {
            this.scratchpad.font         = 'bold 3pt sans-serif';
            this.scratchpad.fillStyle    = 'lightgrey';
            this.scratchpad.textAlign    = 'center';
            this.scratchpad.textBaseline = 'middle';

            if (lock == 25)
            {
              lock = 'B'
            }
            this.scratchpad.fillText (lock,
                                      0,
                                      0);
            this.scratchpad.translate (spacing_small, 0);
          }

        }
        this.scratchpad.restore ();
      }

      // Players
      this.scratchpad.translate (0, spacing_small);
      for (let p = 0; p < 8; p++)
      {
        if (p < players.length)
        {
          let player = players[p];

          if (!game_over && (player['thrower'] == true))
          {
            thrower = player;

            this.scratchpad.save ();
            this.scratchpad.fillStyle = 'black';
            this.scratchpad.fillRect (-spacing_small, -spacing_small*0.6, 100, spacing_small);
            this.scratchpad.restore ();
          }

          this.scratchpad.save ();
          {
            {
              this.scratchpad.font         = 'bold 5px sans-serif';
              this.scratchpad.fillStyle    = 'darkgrey';
              this.scratchpad.textAlign    = 'center';
              this.scratchpad.textBaseline = 'middle';
              this.scratchpad.fillText (player.name,
                                        0,
                                        0);
            }

            if (!game_over)
            {
              this.scratchpad.translate (spacing_small, 0);

              for (let l in player.scoreboard.locks)
              {
                let scored = player.scoreboard.locks[l];

                this.scratchpad.translate (spacing_small, 0);

                this.scratchpad.save ();
                {
                  this.scratchpad.drawImage (GamePanel.lock_images[scored],
                                             -spacing_small/4,
                                             -spacing_small/4,
                                             spacing_small/2,
                                             spacing_small/2);
                }
                this.scratchpad.restore ();
              }
            }

            this.scratchpad.translate (spacing_small, 0);
            this.scratchpad.translate (spacing_small, 0);
            this.scratchpad.translate (spacing_small, 0);

            {
              this.scratchpad.font = 'bold 5px sans-serif';
              this.scratchpad.fillText (player.score,
                                        0,
                                        0);
            }
          }
          this.scratchpad.restore ();
        }
        this.scratchpad.translate (0, spacing_small);
      }

      this.scratchpad.translate (spacing_small, spacing_small);

      if (game_over)
      {
        this.scratchpad.drawImage (GamePanel.images['podium'],
                                   spacing_big,
                                   -spacing_big,
                                   spacing_big*2.5,
                                   spacing_big*2.5);
      }
      else if (thrower)
      {
        this.scratchpad.save ();
        this.scratchpad.translate (0, spacing_small/4);

        for (let i = 3 - thrower['darts_used']; i > 0; i--)
        {
          this.scratchpad.translate (spacing_big, 0);
          this.scratchpad.drawImage (GamePanel.images['dart'],
                                     0,
                                     0,
                                     spacing_big,
                                     spacing_big);
        }
        this.scratchpad.restore ();

        this.scratchpad.translate (6*spacing_big, spacing_big);
        this.scratchpad.font = 'bold 10pt sans-serif';
        this.scratchpad.textAlign = 'right';
        this.scratchpad.fillStyle = 'black';
        this.scratchpad.fillText (data['rounds_to_go'],
                                  0,
                                  0);
      }

    }
    this.stopDrawing ();
  }
}
