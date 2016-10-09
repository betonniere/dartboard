// -----------------------------------------
function draw (focus_point, focus_power)
{
  var canvas = document.getElementById ('dartboard_canvas');

  if (canvas.getContext)
  {
    var ctx = canvas.getContext ('2d');
    var safe_area = 8;
    var size;

    if (canvas.width <= canvas.height)
    {
      size = canvas.width;
    }
    else
    {
      size = canvas.height;
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

    ctx.save ();
    ctx.rotate (-Math.PI/2 + 2*Math.PI/20);
    ctx.strokeStyle = "rgb(100,100,100)";
    // Simple sectors
    for (var i = 0; i < 20; i++)
    {
      var sector = simpleSector (canvas, i, safe_area);

      if ((focus_power == 1) && (focus_point == i+1))
      {
        ctx.fillStyle = "orange";
      }
      else if (i%2 == 0)
      {
        ctx.fillStyle   = "rgb(100,100,100)";
      }
      else
      {
        ctx.fillStyle   = "rgb(230,230,230)";
      }
      ctx.stroke (sector);
      ctx.fill   (sector);
    }

    // Power sectors
    ctx.lineWidth = 3;
    for (var power = 2; power <= 3; power++)
    {
      for (var i = 0; i < 20; i++)
      {
        var sector = smallSector (canvas, i, safe_area, power, ctx.lineWidth);

        if ((focus_power == power) && (focus_point == i+1))
        {
          ctx.strokeStyle = "orange";
        }
        else if (i%2 == 0)
        {
          ctx.strokeStyle = "rgb(0,0,200)";
        }
        else
        {
          ctx.strokeStyle = "rgb(200,0,0)";
        }
        ctx.stroke (sector);
      }
    }
    ctx.restore ();

    ctx.restore ();
  }
}

// -----------------------------------------
function simpleSector (canvas, i, safe_area)
{
  var sector = new Path2D ();
  var angle  = 2*Math.PI/20;

  sector.arc (0, 0, 50-safe_area,
              i*angle - Math.PI/20,
              (i+1)*angle - Math.PI/20,
              false);

  sector.lineTo (0, 0);

  return sector;
}

// -----------------------------------------
function smallSector (canvas, i, safe_area, power, width)
{
  var sector = new Path2D ();
  var angle  = 2*Math.PI/20;
  var radius;

  if (power == 2)
  {
    radius = (50-safe_area)/2 + (width/2);
  }
  else
  {
    radius = 50-safe_area - (width/2);
  }

  sector.arc (0, 0, radius,
              i*angle - Math.PI/20,
              (i+1)*angle - Math.PI/20,
              false);

  return sector;
}
