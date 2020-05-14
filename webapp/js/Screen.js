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

class Screen
{
  // ----
  constructor (canvas_id,
               error_id)
  {
    this.canvas_id = canvas_id;
    this.error_id  = error_id;
  }

  // ----
  connect ()
  {
    this.socket = new WebSocket ("ws://" + document.domain + ":" + location.port + "/websocket");

    let context = this;
    this.socket.onopen    = function ()    {context.onConnected    ();};
    this.socket.onclose   = function ()    {context.onDisconnected ();};
    this.socket.onmessage = function (msg) {context.onMessage      (msg);};
  }

  // ----
  onConnected ()
  {
    let board_size;

    this.error = document.getElementById (this.error_id);
    this.error.style.display = 'none';

    this.canvas = document.getElementById (this.canvas_id);
    this.canvas.width  = window.innerWidth;
    this.canvas.height = window.innerHeight;

    this.scratchpad = this.canvas.getContext ('2d');

    this.board = new Board     (this.scratchpad, this.socket);
    this.panel = new GamePanel (this.scratchpad, this.socket);

    if (this.canvas.width <= this.canvas.height)
    {
      board_size = Math.min (this.canvas.width, this.canvas.height*0.5);
      this.panel.setPosition (0, 100);
    }
    else
    {
      board_size = Math.min (this.canvas.height, this.canvas.width*0.5);
      this.panel.setPosition (100, 0);
    }

    this.scratchpad.scale (board_size/100, board_size/100);
    this.board.draw ();
  }

  // ----
  onDisconnected  ()
  {
    this.error.style.display = 'block';
  }

  // ----
  onMessage (msg)
  {
    let json_msg = JSON.parse (msg.data);

    if (json_msg.hasOwnProperty ('msg'))
    {
      if (json_msg['msg'] == 'HELLO')
      {
      }
      else if (json_msg['msg'] == 'GOODBYE')
      {
        this.error.style.display = 'block';
      }
      else if (json_msg['msg'] == 'HIT')
      {
        {
          let sound = document.getElementById ('hit_sound');

          sound.play ();
        }

        this.board.draw (json_msg['number'], json_msg['power']);
      }
      else if (json_msg['msg'] == 'GAME')
      {
        this.panel.draw (json_msg['players']);
      }
    }
  }
}
