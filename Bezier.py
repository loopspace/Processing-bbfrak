class Bezier:
    """A class for manipulating bezier curves."""
    
    def __init__(self,*args):
        """Initialise a bezier curve, either from four vectors or a list of four vectors."""
        if len(args) == 4:
            self.points = args
        else:
            self.points = args[0]
            
    def draw(self):
        """Draw the bezier using the native command."""
        bezier(self.points[0].x,
               self.points[0].y,
               self.points[1].x,
               self.points[1].y,
               self.points[2].x,
               self.points[2].y,
               self.points[3].x,
               self.points[3].y)
    
    def reverse(self):
        return self.__class__(self.points[3],self.points[2],self.points[1],self.points[0])
    
    def point(self,t):
        """Get a point on a bezier curve."""
        s = 1 - t
        a = s*s*s*self.points[0]
        b = 3*s*s*t*self.points[1]
        c = 3*s*t*t*self.points[2]
        d = t*t*t*self.points[3]
        return a + b + c + d
    
    def tangent(self,t):
        """Get a tangent to a bezier curve."""
        s = 1 - t
        a = self.points[0]
        b = self.points[1]
        c = self.points[2]
        d = self.points[3]
        return 3*s*s*(b-a) + 6*s*t*(c-b) + 3*t*t*(d - c)
    
    def length(self,n=100):
        p = 0
        for i in range(n):
            p += self.tangent(float(i)/n).mag()/n
        return p

    def timeToLength(self,t, n = 100):
        """Convert a length along the curve to a time."""
        l = 0
        t *= n
        for i in range(n):
            v = self.tangent(float(i)/n).mag()
            if l + v > t:
                return float(i)/n + (t - l)/v/n
            l += v
        return 1
            
    def split(self,t):
        """Split a bezier curve into two segments by time."""
        s = 1 - t
        a = self.points[0]
        b = self.points[1]
        c = self.tangent(t)
        d = self.point(t)
        e = self.points[2]
        f = self.points[3]
        g = -t/3*c + d
        h = s/3*c + d
        b = t*b + s*a
        e = s*e + t*f
        return self.__class__(a,b,g,d), self.__class__(d,h,e,f)

    def splitAtLength(self,t):
        """Split a bezier curve into two segments by length."""
        t = self.timeToLength(t)
        return self.split(t)

    def drawTo(self,t):
        """Draw the bezier curve up to a point."""
        a = self.points[0]
        b = self.points[1]
        c = self.tangent(t)
        d = self.point(t)
        c = -t/3*c + d
        b = t*b + (1 - t)*a
        bezier(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        
    def drawFrom(self,t):
        """Draw the bezier curve from a point."""
        c = self.tangent(t)
        d = self.point(t)
        e = self.points[2]
        f = self.points[3]
        c = (1-t)/3*c + d
        e = (1 - t)*e + t*f
        bezier(d.x,d.y,c.x,c.y,e.x,e.y,f.x,f.y)
    
    def drawBetween(self,s,t):
        """Draw the bezier curve between two points."""
        a = self.point(s)
        b = self.tangent(s)
        c = self.tangent(t)
        d = self.point(t)
        b = (1-s)/3*b + a
        c = -t/3*c + d
        bezier(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
    
    def drawToLength(self,t, n = 100):
        """Draw the bezier curve up to a given length."""
        t = self.timeToLength(t,n)
        self.drawTo(t)
