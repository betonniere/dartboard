// *****************************************
var Sector = function (id , safe_area)
{
  this.id        = id;
  this.safe_area = safe_area;
  this.path      = new Path2D ();
  this.angle     = 2*Math.PI/20;
};

// -----------------------------------------
Sector.prototype.getColor = function (has_focus)
{
  if (has_focus)
  {
    return "orange";
  }
  return this.rest_color;
};

// -----------------------------------------
Sector.prototype.defineColors = function (even_color, odd_color)
{
  if (this.id%2 == 0)
  {
    this.rest_color = even_color;
  }
  else
  {
    this.rest_color = odd_color;
  }
};




// *****************************************
var BigSector = function (id , safe_area)
{
  this.sector = new Sector (id, safe_area);

  this.sector.defineColors ("rgb(100,100,100)",
                            "rgb(230,230,230)");
};

// -----------------------------------------
BigSector.prototype.hasFocus = function (focus_point, focus_power)
{
  return ((focus_power == 1) && (focus_point == this.sector.id+1));
};

// -----------------------------------------
BigSector.prototype.draw = function (ctx, focus_point, focus_power)
{
  ctx.fillStyle = this.sector.getColor (this.hasFocus (focus_point, focus_power));

  this.sector.path.arc (0, 0, 50-this.sector.safe_area,
                        this.sector.id*this.sector.angle - Math.PI/20,
                        (this.sector.id+1)*this.sector.angle - Math.PI/20,
                        false);

  this.sector.path.lineTo (0, 0);

  ctx.stroke (this.sector.path);
  ctx.fill   (this.sector.path);
};




// *****************************************
var SmallSector = function (id , safe_area, power, width)
{
  this.sector = new Sector (id, safe_area);

  this.sector.defineColors ("rgb(0,0,200)",
                            "rgb(200,0,0)");

  this.power = power;
  this.width = width;

  if (this.power == 2)
  {
    this.radius = (50-safe_area)/2 + (this.width/2);
  }
  else
  {
    this.radius = 50-safe_area - (this.width/2);
  }
};

// -----------------------------------------
SmallSector.prototype.hasFocus = function (focus_point, focus_power)
{
  return ((focus_power == this.power) && (focus_point == this.sector.id+1));
};

// -----------------------------------------
SmallSector.prototype.draw = function (ctx, focus_point, focus_power)
{
  ctx.strokeStyle = this.sector.getColor (this.hasFocus (focus_point, focus_power));
  ctx.lineWidth   = 3;

  this.sector.path.arc (0, 0, this.radius,
                        this.sector.id*this.sector.angle - Math.PI/20,
                        (this.sector.id+1)*this.sector.angle - Math.PI/20,
                        false);

  ctx.stroke (this.sector.path);
};
