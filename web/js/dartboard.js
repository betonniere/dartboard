var dartboard;

// -----------------------------------------
function onLoad ()
{
  var socket = new WebSocket ("ws://localhost:8080/websocket");

  socket.onmessage = function (msg)
  {
    if (msg.data == "HELLO")
    {
      dartboard = new Dartboard ();
    }
    else if (msg.data == "GOODBYE")
    {
      alert (msg.data);
    }
    else
    {
      var param = msg.data.split ('.');

      dartboard.draw (parseInt (param[0]), param[1]);
    }
  };
}

// -----------------------------------------
var Dartboard = function ()
{
  this.canvas = document.getElementById ('dartboard_canvas');
  this.draw (99, 99);
};

// -----------------------------------------
Dartboard.prototype.draw = function (focus_point, focus_power)
{
  if (this.canvas.getContext)
  {
    var ctx = this.canvas.getContext ('2d');
    var safe_area = 8;
    var size;

    if (this.canvas.width <= this.canvas.height)
    {
      size = this.canvas.width;
    }
    else
    {
      size = this.canvas.height;
    }

    ctx.save ();
    ctx.scale     (size/100, size/100);
    ctx.translate (100/2, 100/2);

    // Background
    ctx.arc (0, 0, 50, 0, 2*Math.PI, false);
    ctx.fillStyle = "black";
    ctx.fill   ();

    // Points
    ctx.font         = 'bold 3pt sans-serif';
    ctx.fillStyle    = 'White';
    ctx.textAlign    = 'center'
    ctx.textBaseline = 'middle'
    for (var i = 1; i <= 20; i++)
    {
      ctx.fillText (i.toString (),
                    46*Math.cos((i * 2*Math.PI/20) - Math.PI/2),
                    46*Math.sin((i * 2*Math.PI/20) - Math.PI/2));
    }

    {
      ctx.save ();
      ctx.rotate (-Math.PI/2 + 2*Math.PI/20);
      ctx.strokeStyle = "rgb(100,100,100)";

      // Simple sectors
      for (var i = 0; i < 20; i++)
      {
        var sector = new BigSector (i+1, safe_area);

        sector.draw (ctx, focus_point, focus_power);
      }

      // Power sectors
      for (var power = 2; power <= 3; power++)
      {
        for (var i = 0; i < 20; i++)
        {
          var sector = new SmallSector (i+1, safe_area, power, 3);

          sector.draw (ctx, focus_point, focus_power);
        }
      }
      ctx.restore ();
    }

    // Bull's eye
    for (var power = 1; power <= 2; power++)
    {
      var sector = new BullSector (50*i, safe_area, power);

      sector.draw (ctx, focus_point, focus_power);
    }

    ctx.restore ();
  }
};
