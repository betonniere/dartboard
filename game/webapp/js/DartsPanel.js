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

class DartsPanel extends Panel
{
  static sectors = [1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20];

  // ----
  constructor (scratchpad, socket, listener)
  {
    super (scratchpad, socket, listener);

    this.safe_area = 8;
  }

  // ----
  plug ()
  {
    super.plug ();
    this.draw ();
  }

  // ----
  draw (focus_number, focus_power)
  {
    this.startDrawing ();
    {
      let focus_sector;

      for (let s = 0; s < DartsPanel.sectors.length; s++)
      {
        if (DartsPanel.sectors[s] == focus_number)
        {
          focus_sector = s + 1;
          break;
        }
      }

      this.scratchpad.translate (100/2, 100/2);

      // Background
      this.scratchpad.arc (0, 0, 50, 0, 2*Math.PI, false);
      this.scratchpad.fillStyle = 'black';
      this.scratchpad.fill   ();

      // Numbers
      this.scratchpad.font         = 'bold 3pt sans-serif';
      this.scratchpad.fillStyle    = 'White';
      this.scratchpad.textAlign    = 'center';
      this.scratchpad.textBaseline = 'middle';

      for (let s = 0; s < DartsPanel.sectors.length; s++)
      {
        this.scratchpad.fillText (DartsPanel.sectors[s].toString (),
                                  46*Math.cos(((s + 1) * 2*Math.PI/20) - Math.PI/2),
                                  46*Math.sin(((s + 1) * 2*Math.PI/20) - Math.PI/2));
      }

      // Sectors
      this.scratchpad.save ();
      {
        this.scratchpad.rotate (-Math.PI/2 + 2*Math.PI/20);
        this.scratchpad.strokeStyle = 'rgb(100,100,100)';

        // Big sectors
        for (let s = 0; s < DartsPanel.sectors.length; s++)
        {
          let sector = new BigSector (DartsPanel.sectors[s], this.socket, this.safe_area);

          sector.draw (this.scratchpad, focus_sector, focus_power);
        }

        // Power sectors
        for (let power = 2; power <= 3; power++)
        {
          for (let i = 1; i <= 20; i++)
          {
            let sector = new SmallSector (i+1, this.socket, this.safe_area, power, 3);

            sector.draw (this.scratchpad, focus_sector, focus_power);
          }
        }
      }
      this.scratchpad.restore ();

      // Bull's eye
      for (let power = 1; power <= 2; power++)
      {
        let sector = new BullSector (25, this.socket, this.safe_area, power);

        sector.draw (this.scratchpad, focus_number, focus_power);
      }
    }
    this.stopDrawing ();
  }
}
