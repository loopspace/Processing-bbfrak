import Bezier as bz
from Path import Path
import bbfrak

def setup():
    size(480,480)
    global t, mt, sp, pen, letter, x
    pen = Path()
    pen.addMoveTo(PVector(-.25,-.25))
    pen.addLineTo(PVector(.25,.25))
    #pen.addMoveTo(PVector(.5,.5))
    pen.scale=10
    pen.colour = (0,0,0)
    t = 0
    mt = 0
    for i in range(26):
        mt = max(mt, getattr(bbfrak,chr(97+i)).length)
    sp = 5
    letter = 0
    x = 150

def draw():
    global t, letter, x
    background(255)
    translate(240,240)
    scale(1,-1)
    noFill()
    stroke(0)
    strokeWeight(3)
    translate(x,0)
    for i in range(letter):
        lt = getattr(bbfrak,chr(97+i))
        lt.drawCartesian(pen)
        wd = lt.boundingbox[1].x - lt.boundingbox[0].x + 20
        translate(wd,0)
    if letter < 26:
        lt = getattr(bbfrak,chr(97+letter))
        lt.drawCartesianAtLength(pen,t)
        wd = lt.boundingbox[1].x - lt.boundingbox[0].x + 20
    #saveFrame("frames/bbfrak-####.png")
    t += sp
    x -= sp/mt*wd
    if t > mt:
        if letter < 26:
            letter += 1
        t = 0
    
