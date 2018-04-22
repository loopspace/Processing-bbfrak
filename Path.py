from Bezier import Bezier

MOVETO = 0
LINETO = 1
CURVETO = 2

def renderPath(sgs,s,pen):
    p = PVector(0,0)
    ps = pen.scale
    for sg in sgs:
        for pg in pen.segments:
            pushStyle()
            if len(pg) != 1:
                fill(*pen.colour)
                noStroke()
            else:
                stroke(*pen.colour)
                
            beginShape()
            dp = pg[0][1]*ps
            for g in sg:
                if g[0] == MOVETO:
                    vertex(s*g[1].x + dp.x,s*g[1].y + dp.y)
                    p = g[1]
                elif g[0] == LINETO:
                    vertex(s*g[1].x + dp.x, s*g[1].y + dp.y)
                    p = g[1]
                elif g[0] == CURVETO:
                    bezierVertex(
                        s*g[1][0].x + dp.x, s*g[1][0].y + dp.y,
                        s*g[1][1].x + dp.x, s*g[1][1].y + dp.y,
                        s*g[1][2].x + dp.x, s*g[1][2].y + dp.y)
                    p = g[1][2]
            dp = s*p
            for g in pg:
                if g[0] == MOVETO:
                    p = g[1]
                elif g[0] == LINETO:
                    vertex(ps*g[1].x + dp.x, ps*g[1].y + dp.y)
                    p = g[1]
                elif g[0] == CURVETO:
                    bezierVertex(
                        ps*g[1][0].x + dp.x, ps*g[1][0].y + dp.y,
                        ps*g[1][1].x + dp.x, ps*g[1][1].y + dp.y,
                        ps*g[1][2].x + dp.x, ps*g[1][2].y + dp.y)
                    p = g[1][2]
            dp = ps*p
            pr = MOVETO
            for g in reversed(sg):
                if pr == LINETO:
                    if g[0] == CURVETO:
                        vertex(s*g[1][2].x + dp.x, s*g[1][2].y + dp.y)
                    else:
                        vertex(s*g[1].x + dp.x, s*g[1].y + dp.y)
                    p = g[1]
                elif pr == CURVETO:
                    if g[0] == CURVETO:
                        bezierVertex(
                            s*p[1].x + dp.x, s*p[1].y + dp.y,
                            s*p[0].x + dp.x, s*p[0].y + dp.y,
                            s*g[1][2].x + dp.x, s*g[1][2].y + dp.y)
                    else:
                        bezierVertex(
                            s*p[1].x + dp.x, s*p[1].y + dp.y,
                            s*p[0].x + dp.x, s*p[0].y + dp.y,
                            s*g[1].x + dp.x, s*g[1].y + dp.y)
                p = g[1]
                pr = g[0]
            if pr == CURVETO:
                dp = p[2]*s
            else:
                dp = p*s
            pr = MOVETO
            for g in reversed(pg):
                if pr == LINETO:
                    if g[0] == CURVETO:
                        vertex(ps*g[1][2].x + dp.x, ps*g[1][2].y + dp.y)
                    else:
                        vertex(ps*g[1].x + dp.x, ps*g[1].y + dp.y)
                    p = g[1]
                elif pr == CURVETO:
                    if g[0] == CURVETO:
                        bezierVertex(
                            ps*p[1].x + dp.x, ps*p[1].y + dp.y,
                            ps*p[2].x + dp.x, ps*p[2].y + dp.y,
                            ps*g[1][2].x + dp.x, ps*g[1][2].y + dp.y)
                    else:
                        bezierVertex(
                            ps*p[1].x + dp.x, ps*p[1].y + dp.y,
                            ps*p[2].x + dp.x, ps*p[2].y + dp.y,
                            ps*g[1].x + dp.x, ps*g[1].y + dp.y)
                p = g[1]
                pr = g[0]
            endShape()
            popStyle()

class Path:
    """A class for manipulating a path with multiple segments."""
    
    def __init__(self):
        self.segments = []
        self.length = 0
        self.point = PVector(0,0)
        self.scale = 1
        self.boundingbox = [PVector(0,0), PVector(0,0)]
    
    def addMoveTo(self,p):
        self.segment = []
        self.segments.append(self.segment)
        self.segment.append([MOVETO,p,0])
        self.point = p
        self.updatebb(self.point)
    
    def addMoveRelTo(self,p):
        self.segment = []
        self.segments.append(self.segment)
        self.segment.append([MOVETO,self.point + p,0])
        self.point = self.point + p
        self.updatebb(self.point)
    
    def addLineTo(self,p):
        l = self.point.dist(p)
        self.segment.append([LINETO,p,l])
        self.length += l
        self.point = p
        self.updatebb(self.point)
    
    def addLineRelTo(self,p):
        l = p.mag()
        self.segment.append([LINETO,self.point + p,l])
        self.length += l
        self.point = self.point + p
        self.updatebb(self.point)

    def addCurveTo(self,b,c,d):
        bz = Bezier(self.point,b,c,d)
        l = bz.length()
        self.segment.append([CURVETO,[b,c,d],l])
        bz = Bezier(self.point,b,c,d)
        self.length += l
        self.point = d
        self.updatebb(b)
        self.updatebb(c)
        self.updatebb(d)

    def addCurveRelTo(self,b,c,d):
        bz = Bezier(self.point,self.point + b,d + c,d)
        l = bz.length()
        self.segment.append([CURVETO,[self.point + b,d + c,d],l])
        bz = Bezier(self.point,self.point + b,d + c,d)
        self.length += l
        self.updatebb(self.point + b)
        self.updatebb(d + c)
        self.updatebb(d)
        self.point = d

    def draw(self):
        p = PVector(0,0)
        s = self.scale
        for sg in self.segments:
            for g in sg:
                if g[0] == MOVETO:
                    p = g[1]
                elif g[0] == LINETO:
                    line(s*p.x,s*p.y, s*g[1].x, s*g[1].y)
                    p = g[1]
                elif g[0] == CURVETO:
                    bezier(s*p.x,s*p.y,
                        s*g[1][0].x, s*g[1][0].y,
                        s*g[1][1].x, s*g[1][1].y,
                        s*g[1][2].x, s*g[1][2].y)
                    p = g[1][2]
    
    def drawSegments(self,n):
        p = PVector(0,0)
        s = self.scale
        n = min(len(self.segments),n)
        for i in range(n):
            for g in self.segments[i]:
                if g[0] == MOVETO:
                    p = g[1]
                elif g[0] == LINETO:
                    line(s*p.x,s*p.y, s*g[1].x, s*g[1].y)
                    p = g[1]
                elif g[0] == CURVETO:
                    bezier(s*p.x,s*p.y,
                        s*g[1][0].x, s*g[1][0].y,
                        s*g[1][1].x, s*g[1][1].y,
                        s*g[1][2].x, s*g[1][2].y)
                    p = g[1][2]

    def drawAtLength(self,t):
        p = PVector(0,0)
        s = self.scale
        l = 0
        for sg in self.segments:
            for g in sg:
                if l + g[2] > t:
                    if g[0] == LINETO:
                        t = (t - l)/g[2]
                        q = t * g[1] + (1 - t)* p
                        line(s*p.x,s*p.y, s*q.x, s*q.y)
                    elif g[0] == CURVETO:
                        t = t - l
                        bz = Bezier(s*p,s*g[1][0],s*g[1][1],s*g[1][2])
                        bz.drawToLength(s*t)
                    return
                if g[0] == MOVETO:
                    p = g[1]
                elif g[0] == LINETO:
                    line(s*p.x,s*p.y, s*g[1].x, s*g[1].y)
                    p = g[1]
                elif g[0] == CURVETO:
                    bezier(s*p.x,s*p.y,
                        s*g[1][0].x, s*g[1][0].y,
                        s*g[1][1].x, s*g[1][1].y,
                        s*g[1][2].x, s*g[1][2].y)
                    p = g[1][2]
                l += g[2]
    
    def drawCartesian(self,pen):
        renderPath(self.segments,self.scale,pen)
        
    def drawCartesianAtLength(self,pen,t):
        p = PVector(0,0)
        l = 0
        sgs = []
        for sg in self.segments:
            nsg = []
            sgs.append(nsg)
            for g in sg:
                if l + g[2] > t:
                    if g[0] == LINETO:
                        t = (t - l)/g[2]
                        q = t * g[1] + (1 - t)* p
                        nsg.append([LINETO,q,q.dist(p)])
                    elif g[0] == CURVETO:
                        t = t - l
                        bz = Bezier(p,g[1][0],g[1][1],g[1][2])
                        bza,bzb = bz.splitAtLength(t)
                        nsg.append([CURVETO,[bza.points[1],bza.points[2],bza.points[3]],bza.length])
                    renderPath(sgs,self.scale,pen)
                    return
                nsg.append(g)
                if g[0] == CURVETO:
                    p = g[1][2]
                else:
                    p = g[1]
                l += g[2]
        renderPath(sgs,self.scale,pen)

    def updatebb(self,p):
        self.boundingbox[0].x = min(self.boundingbox[0].x,p.x)
        self.boundingbox[0].y = min(self.boundingbox[0].y,p.y)
        self.boundingbox[1].x = max(self.boundingbox[1].x,p.x)
        self.boundingbox[1].y = max(self.boundingbox[1].y,p.y)
