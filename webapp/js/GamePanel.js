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
  static nb_lock_image = 4;
  static lock_images = {};

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

      for (let i = 0; i < GamePanel.nb_lock_image; i++)
      {
        let image = new Image ();

        image.onload = function () {caller.onImageloaded (i, image)};
        image.src    =  i + '.svg';
      }
    }
  }

  // ----
  onImageloaded (index, image)
  {
    GamePanel.lock_images[index] = image;

    if (Object.keys (GamePanel.lock_images).length >= GamePanel.nb_lock_image)
    {
      this.listener.onPanelReady ();
    }
  }

  // ----
  draw (players)
  {
    let spacing_small = 7;
    let spacing_big   = 2*spacing_small;

    this.startDrawing ();
    {
      this.scratchpad.fillStyle = 'white';
      this.scratchpad.fillRect (0, 0, 100, 100);

      this.scratchpad.translate (spacing_small, spacing_small);

      // Header
      this.scratchpad.save ();
      {
        this.scratchpad.translate (spacing_small, 0);
        this.scratchpad.translate (spacing_small, 0);

        for (let lock in players[1].scoreboard.locks)
        {
          this.scratchpad.font         = 'bold 3pt sans-serif';
          this.scratchpad.fillStyle    = 'darkblue';
          this.scratchpad.textAlign    = 'center';
          this.scratchpad.textBaseline = 'middle';

          this.scratchpad.fillText (lock,
                                    0,
                                    0);
          this.scratchpad.translate (spacing_small, 0);
        }

      }
      this.scratchpad.restore ();

      this.scratchpad.translate (0, spacing_small);
      for (let p in players)
      {
        let player = players[p];

        if (player['focus'] == true)
        {
          this.scratchpad.save ();
          this.scratchpad.fillStyle = 'lightgrey';
          this.scratchpad.fillRect (-spacing_small, -spacing_small*0.6, 100, spacing_small);
          this.scratchpad.restore ();
        }

        this.scratchpad.save ();
        {
          {
            this.scratchpad.font         = 'bold 5px sans-serif';
            this.scratchpad.fillStyle    = 'black';
            this.scratchpad.textAlign    = 'center';
            this.scratchpad.textBaseline = 'middle';
            this.scratchpad.fillText (player.name,
                                      0,
                                      0);
          }

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

          this.scratchpad.translate (spacing_small, 0);
          this.scratchpad.translate (spacing_small, 0);
          this.scratchpad.translate (spacing_small, 0);

          {
            this.scratchpad.font = 'bold 7px sans-serif';
            this.scratchpad.fillText (player.score,
                                      0,
                                      0);
          }
        }
        this.scratchpad.restore ();

        this.scratchpad.translate (0, spacing_big);
      }
    }
    this.stopDrawing ();
  }
}
