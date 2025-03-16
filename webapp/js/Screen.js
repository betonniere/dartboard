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

let screen;

function startGame (canvas_id,
                    error_screen_id)
{
  screen = new Screen (canvas_id,
                       error_screen_id);

  screen.connect ();
}

function reset ()
{
  screen.reset ();
}

function addPlayer ()
{
  screen.addPlayer ();
}

function removePlayer ()
{
  screen.removePlayer ();
}

function nextPlayer ()
{
  screen.nextPlayer ();
}

class Screen
{
  // ----
  constructor (canvas_id,
               error_screen_id)
  {
    this.canvas = document.getElementById (canvas_id);
    this.error  = document.getElementById (error_screen_id);

    this.pending_panels = 0;
  }

  // ----
  reset ()
  {
    this.socket.send ('{"name": "RESET"}');
  }

  // ----
  addPlayer ()
  {
    this.socket.send ('{"name": "ADD_PLAYER"}');
  }

  // ----
  removePlayer ()
  {
    this.socket.send ('{"name": "REMOVE_PLAYER"}');
  }

  // ----
  nextPlayer ()
  {
    this.socket.send ('{"name": "NEXT_PLAYER"}');
  }

  // ----
  connect ()
  {
    this.socket = new WebSocket ("ws://" + document.domain + ":" + location.port + "/websocket");

    let caller = this;
    this.socket.onopen    = function ()    {caller.onConnected    ();};
    this.socket.onclose   = function ()    {caller.onDisconnected ();};
    this.socket.onmessage = function (msg) {caller.onMessage      (msg);};
    this.socket.onerror   = function (msg) {console.log           (msg);};
  }

  // ----
  onConnected ()
  {
    if (!this.darts_panel)
    {
      let dartboard_size;

      this.canvas.width  = window.innerWidth;
      this.canvas.height = window.innerHeight;

      this.scratchpad = this.canvas.getContext ('2d');

      this.darts_panel = new DartsPanel (this.scratchpad, this.socket, this);
      this.game_panel  = new GamePanel  (this.scratchpad, this.socket, this);

      if (this.canvas.width <= this.canvas.height)
      {
        dartboard_size = Math.min (this.canvas.width, this.canvas.height*0.5);

        if (dartboard_size < this.canvas.height/2)
        {
          let offset = (this.canvas.height/2-dartboard_size)/2;

          this.darts_panel.y = offset * 100/dartboard_size;
          this.game_panel.y  = (this.canvas.height/2) * 100/dartboard_size;
        }
        else
        {
          this.game_panel.y = 100;
        }

        if (dartboard_size < this.canvas.width)
        {
          let offset = (this.canvas.width-dartboard_size)/2;

          this.darts_panel.x = offset * 100/dartboard_size;
        }
      }
      else
      {
        dartboard_size = Math.min (this.canvas.height, this.canvas.width*0.5);

        if (dartboard_size < this.canvas.width/2)
        {
          let offset = (this.canvas.width/2-dartboard_size)/2;

          this.darts_panel.x = offset * 100/dartboard_size;
          this.game_panel.x  = (this.canvas.width/2) * 100/dartboard_size;
        }
        else
        {
          this.game_panel.x = 100;
        }

        if (dartboard_size < this.canvas.height)
        {
          let offset = (this.canvas.height-dartboard_size)/2;

          this.darts_panel.y = offset * 100/dartboard_size;
        }
      }

      this.scratchpad.scale (dartboard_size/100, dartboard_size/100);

      this.darts_panel.plug ();
      this.game_panel.plug  ();
    }
    else if (this.pending_panels == 0)
    {
      this.socket.send ('{"name": "READY"}');
    }

    this.error.style.display = 'none';
  }

  // ----
  onDisconnected  ()
  {
    this.error.style.display = 'block';
    this.socket.close ();
    this.reconnect ();
  }

  // ----
  onPanelCreated  (panel)
  {
    this.pending_panels++;
  }

  // ----
  onPanelReady  (panel)
  {
    this.pending_panels--;

    if (this.pending_panels == 0)
    {
      this.socket.send ('{"name": "READY"}');
    }
  }

  // ----
  onMessage (msg)
  {
    let json_msg = JSON.parse (msg.data);

    if (json_msg.hasOwnProperty ('name'))
    {
      if (json_msg['name'] == 'HELLO')
      {
      }
      else if (json_msg['name'] == 'GOODBYE')
      {
        this.error.style.display = 'block';
      }
      else if (json_msg['name'] == 'HIT')
      {
        {
          let sound = document.getElementById ('hit_sound');

          sound.play ();
        }

        this.darts_panel.draw (json_msg['data']['number'], json_msg['data']['power']);
      }
      else if (json_msg['name'] == 'IDLE')
      {
        this.darts_panel.draw (null, null);
      }
      else if (json_msg['name'] == 'GAME')
      {
        this.game_panel.draw (json_msg['data']);
      }
    }
  }

  // ----
  reconnect (reason)
  {
    let caller = this;

    setTimeout (function () {caller.connect ();}, 5000);
  }
}
