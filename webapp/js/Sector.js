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

// ----------------------------------
class Sector
{
  // ----
  constructor (id, socket, safe_area, even_color, odd_color, power)
  {
    this.id        = id;
    this.socket    = socket;
    this.safe_area = safe_area;
    this.path      = new Path2D ();
    this.angle     = 2*Math.PI/20;
    this.power     = power;

    if (this.id%2 == 0)
    {
      this.rest_color = even_color;
    }
    else
    {
      this.rest_color = odd_color;
    }
  }

  // ----
  hasFocus (focus_point, focus_power)
  {
    return (focus_power == this.power) && (focus_point == this.id);
  }

  // ----
  getColor (has_focus)
  {
    if (has_focus)
    {
      return 'orange';
    }
    else
    {
      return this.rest_color;
    }
  }
}

// ----------------------------------
class BigSector extends Sector
{
  // ----
  constructor (id, socket, safe_area)
  {
    super (id,
           socket,
           safe_area,
           '#e0d48b',
           '#312e2e',
           1);
  }

  // ----
  draw (scratchpad, focus_point, focus_power)
  {
    scratchpad.fillStyle = this.getColor (this.hasFocus (focus_point, focus_power));

    this.path.arc (0, 0, 50-this.safe_area,
                   (this.id-1)*this.angle - Math.PI/20,
                   this.id*this.angle - Math.PI/20,
                   false);

    this.path.lineTo (0, 0);

    scratchpad.stroke (this.path);
    scratchpad.fill   (this.path);

    try
    {
      let caller = this;

      scratchpad.addHitRegion ({'path': this.path, 'id': this.id});

      scratchpad.canvas.onclick = function (e)
      {
        if (e.region)
        {
          caller.socket.send ('{"msg": "HIT", "number": ' + e.region + '}');
        }
      };
    }
    catch (e)
    {
      // console.trace(e);
    }
  }
}

// ----------------------------------
class SmallSector extends Sector
{
  // ----
  constructor (id , socket, safe_area, power, width)
  {
    super (id,
           socket,
           safe_area,
           '#d82121',
           '#229d23',
           power);

    this.width = width;

    if (this.power == 3)
    {
      this.radius = (50-safe_area)/2 + (this.width/2);
    }
    else
    {
      this.radius = 50-safe_area - (this.width/2);
    }
  }

  // ----
  draw (scratchpad, focus_point, focus_power)
  {
    scratchpad.strokeStyle = this.getColor (this.hasFocus (focus_point, focus_power));
    scratchpad.lineWidth   = 3;

    this.path.arc (0, 0, this.radius,
                   (this.id-1)*this.angle - Math.PI/20,
                   this.id*this.angle     - Math.PI/20,
                   false);

    scratchpad.stroke (this.path);
  }
}

// ----------------------------------
class BullSector extends Sector
{
  // ----
  constructor (id , socket, safe_area, power)
  {
    super (id,
           socket,
           safe_area,
           '#d82121',
           '#229d23',
           power);

    if (this.power%2 == 0)
    {
      this.rest_color = '#d82121';
    }
    else
    {
      this.rest_color = '#229d23';
    }

    if (this.power == 1)
    {
      this.radius = 6;
    }
    else
    {
      this.radius = 3;
    }
  }

  // ----
  draw (scratchpad, focus_point, focus_power)
  {
    scratchpad.fillStyle = this.getColor (this.hasFocus (focus_point, focus_power));

    this.path.arc (0, 0, this.radius,
                   0,
                   2*Math.PI,
                   false);

    scratchpad.fill (this.path);
  }
}
