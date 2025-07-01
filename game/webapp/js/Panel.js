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

class Panel
{
  // ----
  constructor (scratchpad, socket, listener)
  {
    this.listener   = listener;
    this.scratchpad = scratchpad;
    this.socket     = socket;

    this.x = 0;
    this.y = 0;

    this.listener.onPanelCreated (this);
  }

  // ----
  startDrawing ()
  {
    this.scratchpad.save ();

    this.scratchpad.translate (this.x, this.y);
  }

  // ----
  stopDrawing ()
  {
    this.scratchpad.restore ();
  }

  // ----
  plug ()
  {
    this.listener.onPanelReady (this);
  }
}
