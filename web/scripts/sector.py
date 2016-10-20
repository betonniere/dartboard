from math       import pi
from browser    import window
from browser    import console
from javascript import JSConstructor

#----------------------------------
class Sector:
    # ----
    def __init__ (self, id, safe_area, even_color, odd_color, power):
        Path2D = JSConstructor (window.Path2D)

        self.id        = id
        self.safe_area = safe_area
        self.path      = Path2D ()
        self.angle     = 2*pi/20
        self.power     = power

        if self.id%2 == 0:
            self.rest_color = even_color
        else:
            self.rest_color = odd_color

    # ----
    def hasFocus (self, focus_point, focus_power):
        return (focus_power == self.power) and (focus_point == self.id)

    # ----
    def getColor (self, has_focus):
        if has_focus:
            return 'orange'
        else:
            return self.rest_color


#----------------------------------
class BigSector (Sector):

    # ----
    def __init__ (self, id , safe_area):
        Sector.__init__ (self,
                         id,
                         safe_area,
                         '#e0d48b',
                         '#312e2e',
                         1)

    # ----
    def draw (self, ctx, focus_point, focus_power):
        ctx.fillStyle = self.getColor (self.hasFocus (focus_point, focus_power))

        self.path.arc (0, 0, 50-self.safe_area,
                       (self.id-1)*self.angle - pi/20,
                       self.id*self.angle - pi/20,
                       False)

        self.path.lineTo (0, 0)

        ctx.stroke (self.path)
        ctx.fill   (self.path)


#----------------------------------
class SmallSector (Sector):

    # ----
    def __init__ (self, id , safe_area, power, width):
        Sector.__init__ (self,
                         id,
                         safe_area,
                         '#d82121',
                         '#229d23',
                         power)

        self.width = width

        if self.power == 2:
            self.radius = (50-safe_area)/2 + (self.width/2)
        else:
            self.radius = 50-safe_area - (self.width/2)

    # ----
    def draw (self, ctx, focus_point, focus_power):
        ctx.strokeStyle = self.getColor (self.hasFocus (focus_point, focus_power))
        ctx.lineWidth   = 3

        self.path.arc (0, 0, self.radius,
                       (self.id-1)*self.angle - pi/20,
                       self.id*self.angle     - pi/20,
                       False)

        ctx.stroke (self.path)


#----------------------------------
class BullSector (Sector):

    # ----
    def __init__ (self, id , safe_area, power):
        Sector.__init__ (self,
                         id,
                         safe_area,
                         '#d82121',
                         '#229d23',
                         power)

        if self.power == 1:
            self.radius = 6
        else:
            self.radius = 3

    # ----
    def draw (self, ctx, focus_point, focus_power):
        ctx.fillStyle = self.getColor (self.hasFocus (focus_point, focus_power))

        self.path.arc (0, 0, self.radius,
                       0,
                       2*pi,
                       False);

        ctx.fill (self.path)
